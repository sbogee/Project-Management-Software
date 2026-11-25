"""Server-rendered page routes."""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@router.get("/register")
def register_page(request: Request):
    """Render the registration page."""
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


@router.get("/projects-page")
def projects_page(request: Request):
    """Render the project listing page."""
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
    )


@router.get("/projects-page/{project_id}")
def project_details_page(
    request: Request,
    project_id: int,
):
    """Render the details page for a project."""
    return templates.TemplateResponse(
        request=request,
        name="project_details.html",
        context={
            "project_id": project_id,
        },
    )
