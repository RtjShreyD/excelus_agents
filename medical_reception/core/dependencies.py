from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from configs.config import envs

bearer_scheme = HTTPBearer()

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, envs['AUTH_SECRET_KEY'], algorithms=envs['AUTH_ALGORITHM'])
        return payload
    
    except JWTError as e:
        print(f"Error decoding token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def validate_token(token: str = Depends(bearer_scheme)) -> None:
    decode_jwt_token(token.credentials)