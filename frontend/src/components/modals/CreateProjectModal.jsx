export default function CreateProjectModal({
    show,
    projectName,
    projectDescription,
    onNameChange,
    onDescriptionChange,
    onClose,
    onCreate
}) {
    if (!show) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Create Project</h5>
                        <button className="btn-close" onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label className="form-label">Name</label>
                            <input
                                type="text"
                                className="form-control"
                                value={projectName}
                                onChange={(event) => onNameChange(event.target.value)}/>
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Description</label>
                            <textarea
                                className="form-control"
                                rows="4"
                                value={projectDescription}
                                onChange={(event) => onDescriptionChange(event.target.value)}/>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary" onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-success" onClick={onCreate}>
                            Create
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
