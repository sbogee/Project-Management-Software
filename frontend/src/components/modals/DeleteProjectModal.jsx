export default function DeleteProjectModal({
    show,
    projectName,
    onClose,
    onDelete
}) 
{
    if (!show) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Delete Project</h5>
                        <button className="btn-close"
                                onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <p> Are you sure you want to delete this project?</p>
                        <strong>{projectName}</strong>
                        <div className="mt-3 text-danger">This action cannot be undone.</div>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-danger"
                                onClick={onDelete}>
                            Delete Project
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}