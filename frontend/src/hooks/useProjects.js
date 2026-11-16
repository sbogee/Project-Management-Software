import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function useProjects() {
    const navigate = useNavigate();

    const [projects, setProjects] = useState([]);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [projectDescription, setProjectDescription] = useState("");

    const loadProjects = useCallback(async () => {
        const token = localStorage.getItem("token");
        const response = await fetch("/api/projects", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/");
            return;
        }

        if (!response.ok) {
            navigate("/");
            return;
        }

        setProjects(await response.json());
    }, [navigate]);

    useEffect(() => {
        if (!localStorage.getItem("token")) {
            navigate("/");
            return;
        }

        loadProjects();
    }, [loadProjects, navigate]);

    function getCurrentUserId() {
        const token = localStorage.getItem("token");
        if (!token) return null;

        const payload = JSON.parse(atob(token.split(".")[1]));
        return Number(payload.sub);
    }

    async function createProject() {
        const token = localStorage.getItem("token");
        const response = await fetch("/api/projects", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: projectName,
                description: projectDescription
            })
        });

        if (!response.ok) {
            alert("Failed to create project");
            return;
        }

        setProjectName("");
        setProjectDescription("");
        setShowCreateModal(false);
        loadProjects();
    }

    const currentUserId = getCurrentUserId();

    return {
        ownedProjects: projects.filter(
            project => project.owner_id === currentUserId
        ),
        sharedProjects: projects.filter(
            project => project.owner_id !== currentUserId
        ),
        showCreateModal,
        setShowCreateModal,
        projectName,
        setProjectName,
        projectDescription,
        setProjectDescription,
        createProject,
        openProject: (projectId) => navigate(`/projects/${projectId}`),
        logout: () => {
            localStorage.removeItem("token");
            navigate("/");
        }
    };
}
