from app.engines.ats.analyzers.project_boundary import is_project_title


# ==========================================================
# SPLIT PROJECTS
# ==========================================================

def split_projects(project_text):

    if isinstance(project_text, list):
        project_text = "\n".join(project_text)

    lines = [

        line.strip()

        for line in project_text.splitlines()

        if line.strip()

    ]

    projects = []

    current_project = []

    for line in lines:

        if is_project_title(line):

            if current_project:

                projects.append("\n".join(current_project))

            current_project = [line]

        else:

            current_project.append(line)

    if current_project:

        projects.append("\n".join(current_project))

    return projects