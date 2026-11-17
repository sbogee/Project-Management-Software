function ProjectGroup({
    title,
    projects,
    onOpen
}) 
{
    if (projects.length === 0) return null;
        
    return (
        <>
            <h3 className="mb-3">{title}</h3>
            <div className="table-responsive">
                <table className="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Documents</th>
                            <th width="120">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {projects.map(
                            project => (
                                <tr key={project.id}>
                                    <td>
                                        <strong>{project.name}</strong>
                                    </td>
                                    <td>
                                        <span className="badge bg-secondary">
                                            {project.documents.length}
                                        </span>
                                    </td>
                                    <td>
                                        <button className="btn btn-primary btn-sm"
                                                onClick={() => onOpen(project.id)}>
                                            Open
                                        </button>
                                    </td>
                                </tr>
                            )
                        )}
                    </tbody>
                </table>
            </div>
        </>
    );
}

export default function ProjectsList({
    ownedProjects,
    sharedProjects,
    onOpen
}) {
    if (ownedProjects.length === 0 && sharedProjects.length === 0) {
        return (
            <div className="alert alert-info">
                No projects yet. Create your first project to get started.
            </div>
        );
    }

    return (
        <>
            <ProjectGroup
                title="Owned Projects"
                projects={ownedProjects}
                onOpen={onOpen}/>
            {ownedProjects.length > 0 && sharedProjects.length > 0 && <hr />}
            <ProjectGroup
                title="Shared With Me"
                projects={sharedProjects}
                onOpen={onOpen}/>
        </>
    );
}
