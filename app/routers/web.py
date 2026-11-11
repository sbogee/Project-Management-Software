from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

@router.get("/projects-page")
def projects_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="projects.html"
    )

@router.get("/projects-page/{project_id}")
def project_details_page(
    request: Request,
    project_id: int
):
    return templates.TemplateResponse(
        request=request,
        name="project_details.html",
        context={
            "project_id": project_id
        }
    )