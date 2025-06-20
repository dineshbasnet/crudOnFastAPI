from fastapi import APIRouter, Depends,status
from .schemas import UserCreateModel,UserModel,UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token,decode_token, verify_passwd
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer




auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/singup",response_model=UserModel,status_code = status.HTTP_201_CREATED)
async def create_user_account(
    user_data:UserCreateModel,
    session: AsyncSession=Depends(get_session)
    
):
    email = user_data.email
    
    user_exits = await user_service.user_exits(email,session)
    
    if user_exits:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exits")
        
        
    new_user = await user_service.create_user(user_data, session)
    
    return new_user

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession=Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user(email, session)
    
    if user is not None:
        passwd_valid = verify_passwd(password, user.hash_password)
        
        if passwd_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid': str(user.uid)
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
                
            )
            
            return JSONResponse(
                content={
                    "message":"Login successfully",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                    }
                }
            )
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )
    
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp((expiry_timestamp)) > datetime.now():
        new_access_token = create_access_token(user_data = token_details['user'])

        return JSONResponse(content = {"access_token": new_access_token})
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired token data"
    )
    
    