from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "is_active": current_user.is_active,
    }
