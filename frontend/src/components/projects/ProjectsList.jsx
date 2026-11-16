function ProjectGroup({ title, projects, onOpen }) {
    if (projects.length === 0) return null;

    return (
        <>
            <h3>{title}</h3>
            {projects.map(project => (
                <div key={project.id} className="card mb-3">
                    <div className="card-body">
                        <h5>{project.name}</h5>
                        <button className="btn btn-primary"
                                onClick={() => onOpen(project.id)}>
                            Open
                        </button>
                    </div>
                </div>
            ))}
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
                No projects found.
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
