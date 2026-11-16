import { useNavigate, useParams } from "react-router-dom";
import DeleteDocumentModal from "../components/modals/DeleteDocumentModal";
import DeleteProjectModal from "../components/modals/DeleteProjectModal";
import EditDocumentModal from "../components/modals/EditDocumentModal";
import EditProjectModal from "../components/modals/EditProjectModal";
import InviteMemberModal from "../components/modals/InviteMemberModal";
import UploadDocumentModal from "../components/modals/UploadDocumentModal";
import ProjectDocumentsSection from "../components/projects/ProjectDocumentsSection";
import ProjectMembersSection from "../components/projects/ProjectMembersSection";
import ProjectOverviewSection from "../components/projects/ProjectOverviewSection";
import useProjectDetails from "../hooks/useProjectDetails";

export default function ProjectDetailsPage() {
    const navigate = useNavigate();
    const { projectId } = useParams();
    const details = useProjectDetails(projectId);

    function logout() {
        localStorage.removeItem("token");
        navigate("/");
    }

    if (!details.project) {
        return <div className="container mt-4">Loading...</div>;
    }

    const { project, isProjectOwner } = details;

    return (
        <div className="container mt-4">
            <ProjectOverviewSection
                project={project}
                isOwner={isProjectOwner}
                onBack={() => navigate("/projects")}
                onEdit={() => details.setShowEditProjectModal(true)}
                onDelete={() => details.setShowDeleteProjectModal(true)}
                onLogout={logout}/>

            <ProjectMembersSection
                members={project.member_user_ids}
                canInvite={isProjectOwner}
                onInvite={() => details.setShowInviteModal(true)}/>

            <ProjectDocumentsSection
                documents={project.documents}
                onUpload={() => details.setShowUploadModal(true)}
                onDownload={details.downloadDocument}
                onEdit={(document) => {
                    details.setDocumentToEdit(document);
                    details.setShowEditDocumentModal(true);
                }}
                onDelete={(document) => {
                    details.setDocumentToDelete(document);
                    details.setShowDeleteModal(true);
                }}/>

            <EditProjectModal
                show={details.showEditProjectModal}
                projectName={details.editedProjectName}
                projectDescription={details.editedProjectDescription}
                setProjectName={details.setEditedProjectName}
                setProjectDescription={details.setEditedProjectDescription}
                onClose={() => details.setShowEditProjectModal(false)}
                onSave={details.updateProject}/>

            {isProjectOwner && (
                <DeleteProjectModal
                    show={details.showDeleteProjectModal}
                    projectName={project.name}
                    onClose={() => details.setShowDeleteProjectModal(false)}
                    onDelete={details.deleteProject}/>
            )}

            {isProjectOwner && (
                <InviteMemberModal
                    show={details.showInviteModal}
                    username={details.memberUsername}
                    onUsernameChange={details.setMemberUsername}
                    onClose={() => details.setShowInviteModal(false)}
                    onInvite={details.inviteMember}/>
            )}

            <UploadDocumentModal
                show={details.showUploadModal}
                onFileSelect={(event) => {
                    details.setSelectedFile(event.target.files[0]);
                }}
                onClose={() => details.setShowUploadModal(false)}
                onUpload={details.uploadDocument}/>

            <DeleteDocumentModal
                show={details.showDeleteModal}
                document={details.documentToDelete}
                onClose={() => details.setShowDeleteModal(false)}
                onDelete={details.deleteDocument}/>

            <EditDocumentModal
                show={details.showEditDocumentModal}
                document={details.documentToEdit}
                newDocumentFile={details.newDocumentFile}
                setNewDocumentFile={details.setNewDocumentFile}
                onClose={() => {
                    details.setShowEditDocumentModal(false);
                    details.setDocumentToEdit(null);
                }}
                onSave={details.updateDocument}/>
        </div>
    );
}
