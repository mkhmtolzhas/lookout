from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from src.schemas.user_schema import UserCreate, UserLogin
from src.schemas.responses.auth_response import RefreshResponse
from src.schemas.auth_schema import RefreshBody
from src.usecases.user_usecase import UserUseCase, get_user_use_case
from src.api.http.dependencies import security
from src.schemas.responses.auth_response import AuthResponse


router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(
    user: UserLogin,
    response: Response,
    use_case: UserUseCase = Depends(get_user_use_case),
):
    try:
        user = await use_case.login_user(user=user)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = security.create_access_token(
            uid=user.email,
        )

        refresh_token = security.create_refresh_token(
            uid=user.email,
        )

        response.set_cookie(
            key="access_token_cookie",
            value=access_token,
        )

        response.set_cookie(
            key="refresh_token_cookie",
            value=refresh_token,
        )

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register")
async def register(
    user: UserCreate,
    response: Response,
    use_case: UserUseCase = Depends(get_user_use_case),
):
    """
    User registration endpoint.
    """
    try:
        new_user = await use_case.create_user(user)
        if not new_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        access_token = security.create_access_token(
            uid=new_user.email,
        )

        refresh_token = security.create_refresh_token(
            uid=new_user.email,
        )

        response.set_cookie(
            key="access_token_cookie",
            value=access_token,
        )
        response.set_cookie(
            key="refresh_token_cookie",
            value=refresh_token,
        )

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/logout")
async def logout(
    response: Response,
):
    """
    User logout endpoint.
    """
    try:
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post('/refresh')
async def refresh(
    refresh_payload: TokenPayload = Depends(security.refresh_token_required)
):
    access_token = security.create_access_token(
        refresh_payload.sub,
    )
    return RefreshResponse(
        access_token=access_token
    )


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected_route():
    """
    Protected route example.
    """
    try:
        return {"message": f"Hello, bro!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
