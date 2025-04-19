from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.payment import router as payment_router
from .endpoints.logs import router as logs_router


router = APIRouter(prefix="/v1")


router.include_router(auth_router)
router.include_router(payment_router)
router.include_router(logs_router)
