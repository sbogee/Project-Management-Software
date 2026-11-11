const projectId = document.body.dataset.projectId;

async function deleteDocument(documentId) {

    const confirmed = confirm(
        "Are you sure you want to delete this document?"
    );

    if (!confirmed) {
        return;
    }

    const token =
        localStorage.getItem("token");

    const response =
        await fetch(
            `/documents/${documentId}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

    if (!response.ok) {

        alert(
            "Failed to delete document."
        );

        return;
    }

    await loadProject();
}

async function uploadDocument() {

    const token =
        localStorage.getItem("token");

    const fileInput =
        document.getElementById(
            "documentFile"
        );

    const file =
        fileInput.files[0];

    if (!file) {

        alert(
            "Please select a file."
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            `/projects/${projectId}/documents`,
            {
                method: "POST",
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                },
                body: formData
            }
        );

    if (!response.ok) {

        alert(
            "Failed to upload document."
        );

        return;
    }

    const modal =
        bootstrap.Modal.getInstance(
            document.getElementById(
                "uploadDocumentModal"
            )
        );

    modal.hide();

    fileInput.value = "";

    alert(
        "Document uploaded successfully."
    );

    await loadProject();
}

async function deleteProject() {

    const confirmed = confirm(
        "Are you sure you want to delete this project?"
    );

    if (!confirmed) {
        return;
    }

    const token =
        localStorage.getItem("token");

    const response =
        await fetch(
            `/projects/${projectId}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

    if (!response.ok) {

        alert(
            "Failed to delete project"
        );

        return;
    }

    alert(
        "Project deleted successfully"
    );

    window.location.href =
        "/projects-page";
}

async function updateProject() {

    const token =
        localStorage.getItem("token");

    const name =
        document.getElementById(
            "editProjectName"
        ).value;

    const description =
        document.getElementById(
            "editProjectDescription"
        ).value;

    const response =
        await fetch(
            `/projects/${projectId}/info`,
            {
                method: "PUT",
                headers: {
                    "Authorization":
                        `Bearer ${token}`,
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    name,
                    description
                })
            }
        );

    if (!response.ok) {

        alert(
            "Failed to update project"
        );

        return;
    }

    const modal =
        bootstrap.Modal.getInstance(
            document.getElementById(
                "editProjectModal"
            )
        );

    modal.hide();

    await loadProject();
}

async function loadProject(){

    const token =
        localStorage.getItem("token");

    const response =
        await fetch(
            `/projects/${projectId}/info`,
            {
                headers:{
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

    if(!response.ok){
        alert(
            "Cannot load project"
        );
        return;
    }

    const tmp_project = await response.json();
    const project = tmp_project[0]
    console.log(project)

    document.getElementById(
        "projectName"
    ).innerText =
        project.name;

    document.getElementById(
        "projectDescription"
    ).innerText =
        project.description;

    document.getElementById(
        "editProjectName"
    ).value =
        project.name;

    document.getElementById(
        "editProjectDescription"
    ).value =
        project.description;

    document.getElementById(
        "owner"
    ).innerText =
        project.owner_id;

    const memberTitle = document.getElementById("membersTitle");
    let memberCount = 0
    const memberList =
        document.getElementById(
            "memberList"
        );
    memberList.innerHTML = "";
    project.member_user_ids.forEach(member => {
        if (member != project.owner_id)
        {
            memberList.innerHTML +=
            `<li>${member}</li>`;
            memberCount++;
        }
    });

    const documentList =
    document.getElementById(
        "documentList"
    );
    const separator = document.getElementById("separator");
    documentList.innerHTML = "";
    project.documents.forEach(document => {
        documentList.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center">

                <span>
                    ${document.filename}
                </span>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="deleteDocument(${document.id})"
                >
                    Delete
                </button>

            </li>
        `;
    });

    memberTitle.textContent = memberCount > 0 ? "Members" : "";
    separator.style.display = memberCount > 0 ? "block" : "none";
}

loadProject();