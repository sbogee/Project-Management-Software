export default function EditDocumentModal({
    show,
    document,
    newDocumentFile,
    setNewDocumentFile,
    onClose,
    onSave
})
{
    if (!show || !document) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Edit Document</h5>
                        <button className="btn-close"
                                onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <p>Current document:</p>
                        <strong>{document.filename}</strong>
                        <hr /> 

                        <input type="file"
                               className="form-control"
                               onChange={(e) => setNewDocumentFile(e.target.files[0])}/>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-warning"
                                onClick={onSave}>
                            Replace File
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}