export default function ProjectDocumentsSection({
    documents,
    onUpload,
    onDownload,
    onEdit,
    onDelete
}) {
    return (
        <>
            <h4>Documents</h4>
            <div className="mb-3">
                <button className="btn btn-success" onClick={onUpload}>
                    Upload Document
                </button>
            </div>
            {documents.map(document => (
                <div key={document.id}
                     className="d-flex justify-content-between align-items-center mb-2">
                    <span>{document.filename}</span>
                    <div>
                        <button className="btn btn-primary btn-sm me-2"
                                onClick={() => onDownload(document.id)}>
                            Download
                        </button>
                        <button className="btn btn-warning btn-sm me-2"
                                onClick={() => onEdit(document)}>
                            Edit
                        </button>
                        <button className="btn btn-danger btn-sm"
                                onClick={() => onDelete(document)}>
                            🗑️
                        </button>
                    </div>
                </div>
            ))}
        </>
    );
}
