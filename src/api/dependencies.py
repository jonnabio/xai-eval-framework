from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.api.config import settings
from src.api.models.schemas import TokenData, User

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validate the JWT token and return the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode token
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "user")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username, role=role)
        
    except JWTError:
        raise credentials_exception
    
    # In a full system, we would query the database to ensure the user still exists / is active.
    # For Phase 1, we rely on the token claims being valid.
    user = User(username=username, role=role, disabled=False)
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure the current user has 'admin' role.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The user doesn't have enough privileges"
        )
    return current_user
