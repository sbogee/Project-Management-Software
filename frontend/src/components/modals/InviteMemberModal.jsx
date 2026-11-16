export default function InviteMemberModal({
    show,
    username,
    onUsernameChange,
    onClose,
    onInvite
}) 
{
    if (!show) return null;

    return (
        <div className="modal d-block"
             style={{backgroundColor: "rgba(0,0,0,0.5)"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5>Invite Member</h5>
                        <button className="btn-close"
                                onClick={onClose}/>
                    </div>
                    <div className="modal-body">
                        <label className="form-label">Username</label>
                        <input className="form-control"
                               value={username}
                               onChange={(event) => onUsernameChange(event.target.value)}/>
                    </div>
                    <div className="modal-footer">
                        <button className="btn btn-secondary"
                                onClick={onClose}>
                            Cancel
                        </button>
                        <button className="btn btn-success"
                                onClick={onInvite}>
                            Invite
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
