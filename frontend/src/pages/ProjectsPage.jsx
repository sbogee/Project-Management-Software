import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ProjectsPage() {

    const navigate = useNavigate();

    const [projects, setProjects] = useState([]);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [projectDescription, setProjectDescription] = useState("");

    useEffect(() => {

        const token =
            localStorage.getItem("token");

        if (!token) {

            navigate("/");

            return;
        }

        loadProjects();

    }, []);

    async function loadProjects() {

        const token =
            localStorage.getItem("token");

        const response =
            await fetch(
                "http://localhost:8000/projects",
                {
                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

        if (!response.ok) {

            navigate("/");

            return;
        }

        const data =
            await response.json();

        setProjects(data);
    }

    function getCurrentUserId() {

        const token =
            localStorage.getItem("token");

        if (!token) {
            return null;
        }

        const payload =
            JSON.parse(
                atob(
                    token.split(".")[1]
                )
            );

        return Number(payload.sub);
    }

    function openProject(projectId) {

        navigate(
            `/projects/${projectId}`
        );
    }

    function logout() {

        localStorage.removeItem("token");

        navigate("/");
    }

    async function createProject()
    {
        const token = localStorage.getItem("token");

        const response = await fetch("http://localhost:8000/projects",
            {
                method: "POST",
                headers: 
                {
                    Authorization:
                        `Bearer ${token}`,
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    name: projectName,
                    description: projectDescription
                })
            }
        );

        if (!response.ok)
        {
            alert("Failed to create project");
            return;
        }

        setProjectName("");
        setProjectDescription("");

        setShowCreateModal(false);

        loadProjects();
    }

    const userId =
        getCurrentUserId();

    const ownedProjects =
        projects.filter(
            project =>
                project.owner_id === userId
        );

    const participantProjects =
        projects.filter(
            project =>
                project.owner_id !== userId
        );

    return (

        <div className="container mt-4">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <h2>Projects</h2>
                <button
                    className="btn btn-success me-2"
                    onClick={() => setShowCreateModal(true)}
                >
                    Create Project
                </button>
                <button
                    className="btn btn-outline-danger"
                    onClick={logout}
                >
                    Logout
                </button>

            </div>


            {ownedProjects.length > 0 && (

                <>
                    <h3>
                        Owned Projects
                    </h3>

                    {
                        ownedProjects.map(
                            project => (

                                <div
                                    key={project.id}
                                    className="card mb-3"
                                >

                                    <div className="card-body">

                                        <h5>
                                            {project.name}
                                        </h5>

                                        <button
                                            className="btn btn-primary"
                                            onClick={() =>
                                                openProject(
                                                    project.id
                                                )
                                            }
                                        >
                                            Open
                                        </button>

                                    </div>

                                </div>

                            )
                        )
                    }
                </>
            )}


            {
                ownedProjects.length > 0 &&
                participantProjects.length > 0 &&
                <hr />
            }


            {participantProjects.length > 0 && (

                <>
                    <h3>
                        Shared With Me
                    </h3>

                    {
                        participantProjects.map(
                            project => (

                                <div
                                    key={project.id}
                                    className="card mb-3"
                                >

                                    <div className="card-body">

                                        <h5>
                                            {project.name}
                                        </h5>

                                        <button
                                            className="btn btn-primary"
                                            onClick={() =>
                                                openProject(
                                                    project.id
                                                )
                                            }
                                        >
                                            Open
                                        </button>

                                    </div>

                                </div>

                            )
                        )
                    }
                </>
            )}

            {ownedProjects.length === 0 &&
            participantProjects.length === 0 &&
                (
                    <div className="alert alert-info">

                        No projects found.

                    </div>
                )
            }

            {showCreateModal &&
                <div
                className="modal d-block"
                style={{
                    backgroundColor:
                        "rgba(0,0,0,0.5)"
                }}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5>Create Project</h5>
                                <button
                                    className="btn-close"
                                    onClick={() =>
                                        setShowCreateModal(false)
                                    }
                                />
                            </div>
                            <div className="modal-body">
                                ...
                            </div>
                        </div>
                    </div>
                </div>
            }

        </div>
    );
}