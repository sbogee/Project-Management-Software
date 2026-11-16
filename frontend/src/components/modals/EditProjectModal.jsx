export default function EditProjectModal({
    show,
    projectName,
    projectDescription,
    setProjectName,
    setProjectDescription,
    onClose,
    onSave
}) 
{
    if (!show) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Update Project</h5>
                        <button className="btn-close"
                                onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <input className="form-control mb-3"
                               value={projectName}
                               onChange={(e) => setProjectName(e.target.value)}/>
                        <textarea className="form-control"
                                  value={projectDescription}
                                  onChange={(e) =>setProjectDescription(e.target.value)}/>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-warning"
                                onClick={onSave}>
                            Save
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}