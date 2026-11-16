import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function useProjectDetails(projectId) {
    const navigate = useNavigate();

    const [project, setProject] = useState(null);
    const [showUploadModal, setShowUploadModal] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [documentToDelete, setDocumentToDelete] = useState(null);
    const [showInviteModal, setShowInviteModal] = useState(false);
    const [memberUsername, setMemberUsername] = useState("");
    const [showEditDocumentModal, setShowEditDocumentModal] = useState(false);
    const [documentToEdit, setDocumentToEdit] = useState(null);
    const [newDocumentFile, setNewDocumentFile] = useState(null);
    const [showEditProjectModal, setShowEditProjectModal] = useState(false);
    const [showDeleteProjectModal, setShowDeleteProjectModal] = useState(false);
    const [editedProjectName, setEditedProjectName] = useState("");
    const [editedProjectDescription, setEditedProjectDescription] = useState("");

    const loadProject = useCallback(async () => {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/projects/${projectId}/info`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/");
            return;
        }

        if (!response.ok) {
            navigate("/projects");
            return;
        }

        const [data] = await response.json();
        setProject(data);
        setEditedProjectName(data.name);
        setEditedProjectDescription(data.description);
    }, [navigate, projectId]);

    useEffect(() => {
        loadProject();
    }, [loadProject]);

    function getCurrentUserId() {
        const token = localStorage.getItem("token");
        if (!token) return null;

        const payload = JSON.parse(atob(token.split(".")[1]));
        return Number(payload.sub);
    }

    async function uploadDocument() {
        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }

        const token = localStorage.getItem("token");
        const formData = new FormData();
        formData.append("file", selectedFile);

        const response = await fetch(`/api/projects/${projectId}/documents`,
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        if (!response.ok) {
            alert("Failed to upload document.");
            return;
        }

        setShowUploadModal(false);
        setSelectedFile(null);
        loadProject();
    }

    async function deleteDocument() {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/documents/${documentToDelete.id}`,
            {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            alert("Failed to delete document.");
            return;
        }

        setShowDeleteModal(false);
        setDocumentToDelete(null);
        loadProject();
    }

    async function inviteMember() {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/projects/${projectId}/invite?user=${memberUsername}`,
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            const error = await response.json();
            alert(error.detail);
            return;
        }

        setMemberUsername("");
        setShowInviteModal(false);
        await loadProject();
    }

    async function downloadDocument(documentId) {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/documents/${documentId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            alert("Failed to download document.");
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;

        const disposition = response.headers.get("content-disposition");
        let filename = "document";
        if (disposition) {
            const match = disposition.match(/filename="?([^"]+)"?/);
            if (match) filename = match[1];
        }

        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    }

    async function updateDocument() {
        const token = localStorage.getItem("token");
        const formData = new FormData();
        formData.append("file", newDocumentFile);

        const response = await fetch(`/api/documents/${documentToEdit.id}`,
            {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        if (!response.ok) {
            alert("Failed to update document.");
            return;
        }

        setShowEditDocumentModal(false);
        loadProject();
    }

    async function updateProject() {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/projects/${projectId}/info`,
            {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: editedProjectName,
                    description: editedProjectDescription
                })
            }
        );

        if (!response.ok) {
            alert("Failed to update project.");
            return;
        }

        setShowEditProjectModal(false);
        await loadProject();
    }

    async function deleteProject() {
        const token = localStorage.getItem("token");
        const response = await fetch(`/api/projects/${projectId}`,
            {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            alert("Failed to delete project.");
            return;
        }

        navigate("/projects");
    }

    const isProjectOwner = project
        ? project.owner_id === getCurrentUserId()
        : false;

    return {
        project,
        isProjectOwner,
        showUploadModal,
        setShowUploadModal,
        selectedFile,
        setSelectedFile,
        showDeleteModal,
        setShowDeleteModal,
        documentToDelete,
        setDocumentToDelete,
        showInviteModal,
        setShowInviteModal,
        memberUsername,
        setMemberUsername,
        showEditDocumentModal,
        setShowEditDocumentModal,
        documentToEdit,
        setDocumentToEdit,
        newDocumentFile,
        setNewDocumentFile,
        showEditProjectModal,
        setShowEditProjectModal,
        showDeleteProjectModal,
        setShowDeleteProjectModal,
        editedProjectName,
        setEditedProjectName,
        editedProjectDescription,
        setEditedProjectDescription,
        uploadDocument,
        deleteDocument,
        inviteMember,
        downloadDocument,
        updateDocument,
        updateProject,
        deleteProject
    };
}
