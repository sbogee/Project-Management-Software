"""Administrative API endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def get_admin_dashboard():
    """Return the admin dashboard status."""
    return {"message": "Admin Dashboard"}
