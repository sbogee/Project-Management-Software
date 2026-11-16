export default function ProjectsHeader({ onCreate, onLogout }) 
{
    return (
        <div className="d-flex justify-content-between align-items-center mb-4">
            <h2>Projects</h2>
            <div>
                <button className="btn btn-success me-2" onClick={onCreate}>
                    Create Project
                </button>
                <button className="btn btn-outline-danger" onClick={onLogout}>
                    Logout
                </button>
            </div>
        </div>
    );
}
