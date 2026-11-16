import CreateProjectModal from "../components/modals/CreateProjectModal";
import ProjectsHeader from "../components/projects/ProjectsHeader";
import ProjectsList from "../components/projects/ProjectsList";
import useProjects from "../hooks/useProjects";

export default function ProjectsPage() {
    const projects = useProjects();

    return (
        <div className="container mt-4">
            <ProjectsHeader
                onCreate={() => projects.setShowCreateModal(true)}
                onLogout={projects.logout}/>

            <ProjectsList
                ownedProjects={projects.ownedProjects}
                sharedProjects={projects.sharedProjects}
                onOpen={projects.openProject}/>

            <CreateProjectModal
                show={projects.showCreateModal}
                projectName={projects.projectName}
                projectDescription={projects.projectDescription}
                onNameChange={projects.setProjectName}
                onDescriptionChange={projects.setProjectDescription}
                onClose={() => projects.setShowCreateModal(false)}
                onCreate={projects.createProject}/>
        </div>
    );
}
