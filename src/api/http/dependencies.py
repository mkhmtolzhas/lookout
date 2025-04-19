from src.core.config import auth_settings
from authx import AuthX

security = AuthX(
    config=auth_settings,
)