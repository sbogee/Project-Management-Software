function openProject(projectId)
{
    window.location.href =`/projects-page/${projectId}`;
}

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

function getCurrentUserId() {
    const token = localStorage.getItem("token");

    if (!token) return null;

    const payload = token.split(".")[1];
    const decoded = JSON.parse(atob(payload));

    return decoded.sub;
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

    const userId = getCurrentUserId();
    const projects = await response.json();
    console.log(projects);
    console.log(userId);

    const ownedContainer = document.getElementById("ownedProjects");
    const ownedContainerTitle = document.getElementById("ownedProjectsTitle");
    const participantContainer = document.getElementById("participantProjects");
    const participantContainerTitle = document.getElementById("participantProjectsTitle");
    const separator = document.getElementById("separator");

    ownedContainer.innerHTML = "";
    participantContainer.innerHTML = "";

    let ownedCount = 0;
    let participantCount = 0;

    projects.forEach(project => 
    {
        const card = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5>${project.name}</h5>
                    <button
                        class="btn btn-primary"
                        onclick="openProject(${project.id})"
                    >
                        Open
                    </button>
                </div>
            </div>`;

        if (project.owner_id == userId) 
        {
            ownedContainer.innerHTML += card;
            ownedCount++;
        }
        else 
        {
            participantContainer.innerHTML += card;
            participantCount++;
        }
    });

    ownedContainerTitle.textContent = ownedCount > 0 ? "Owned Projects" : "";
    participantContainerTitle.textContent = participantCount > 0 ? "Shared With Me" : "";
    separator.style.display = ownedCount > 0 && participantCount > 0 ? "block" : "none";
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