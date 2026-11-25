export default function DeleteDocumentModal({
    show,
    document,
    onClose,
    onDelete
}) 
{
    if (!show || !document) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Delete Document</h5>
                    </div>
                    <div className="modal-body">
                        Are you sure you want to delete
                        <strong>{" "}{document.filename}</strong>?
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-danger"
                                onClick={onDelete}>
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
