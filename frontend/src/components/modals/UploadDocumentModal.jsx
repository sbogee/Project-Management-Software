export default function UploadDocumentModal({
    show,
    onFileSelect,
    onClose,
    onUpload
}) 
{
    if (!show) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Upload Document</h5>
                        <button className="btn-close"
                                onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <input type="file"
                               className="form-control"
                               onChange={onFileSelect}/>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-success"
                                onClick={onUpload}>
                            Upload
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
