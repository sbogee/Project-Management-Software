export default function ProjectOverviewSection({
    project,
    isOwner,
    onBack,
    onEdit,
    onDelete,
    onLogout
}) {
    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <button className="btn btn-secondary mb-3" onClick={onBack}>
                    Back
                </button>
                <button className="btn btn-outline-danger"
                        onClick={onLogout}>
                    Logout
                </button>
            </div>
            <h2>{project.name}</h2>
            <div className="mb-3">
                <button className="btn btn-warning me-2" onClick={onEdit}>
                    Update Project Info
                </button>
                {isOwner && (
                    <button className="btn btn-danger" onClick={onDelete}>
                        Delete Project
                    </button>
                )}
            </div>
            <p>{project.description}</p>
            <hr />
            <h4>Owner</h4>
            <p>{project.owner_id}</p>
            <hr />
        </>
    );
}
