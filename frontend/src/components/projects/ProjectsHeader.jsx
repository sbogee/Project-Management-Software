export default function ProjectsHeader({ onCreate, onLogout }) 
{
    return (
        <div className="d-flex justify-content-between align-items-center mb-4 position-relative">
            <h2 className="mb-0">Projects</h2>
            <button
                className="btn btn-success position-absolute top-50 start-50 translate-middle"
                onClick={onCreate}>
                Create Project
            </button>
            <button className="btn btn-outline-danger" onClick={onLogout}>
                Logout
            </button>
        </div>
    );
}
