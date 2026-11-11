function checkAuthentication() 
{
    const token = localStorage.getItem("token");
    if (!token) 
    {
        window.location.replace("/");
        return false;
    }
    return true;
}

function logout()
{
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.replace("/");
}

async function loadProjects() 
{
    const token = localStorage.getItem("token");

    const response = await fetch(
        "/projects",
        {
            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    if (!response.ok) 
    {
        if (response.status === 401) logout();
        return;
    }

    const projects = await response.json();

    const container = document.getElementById("projects");

    container.innerHTML = "";

    projects.forEach(project => {
        container.innerHTML += `
            <div class="card mb-3">
                <div class="card-body">
                    <h5>${project.name}</h5>
                    <p>
                        ${project.description}
                    </p>
                    <small>
                        Documents:
                        ${project.documents.length}
                    </small>
                </div>
            </div>
        `;
    });
}

async function createProject() 
{
    const token =
        localStorage.getItem("token");

    const name =
        document.getElementById(
            "projectName"
        ).value;

    const description =
        document.getElementById(
            "projectDescription"
        ).value;

    const response =
        await fetch(
            "/projects",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json",
                    "Authorization":
                        `Bearer ${token}`
                },
                body: JSON.stringify({
                    name,
                    description
                })
            }
        );

    if(response.ok){

        const modal =
            bootstrap.Modal.getInstance(
                document.getElementById(
                    "createProjectModal"
                )
            );

        modal.hide();

        document.getElementById(
            "projectName"
        ).value = "";

        document.getElementById(
            "projectDescription"
        ).value = "";

        loadProjects();
    }
    else{
        alert(
            "Failed to create project"
        );
    }
}

document.addEventListener("DOMContentLoaded", () => 
{
    if (!checkAuthentication())  return;
    loadProjects();
});

window.addEventListener("pageshow", () => 
{
    checkAuthentication();
});