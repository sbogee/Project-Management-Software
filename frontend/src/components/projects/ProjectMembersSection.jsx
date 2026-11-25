export default function ProjectMembersSection({
    members,
    canInvite,
    onInvite
}) {
    return (
        <>
            <h4>Members</h4>
            {canInvite && (
                <div className="mb-3">
                    <button className="btn btn-success" onClick={onInvite}>
                        Invite Member
                    </button>
                </div>
            )}
            {members.map(member => (
                <div key={member}>{member}</div>
            ))}
            <hr />
        </>
    );
}
