from app.parsers.pdf_reader import extract_text_from_pdf

from app.engines.ats.section.resume_cleaner import clean_resume
from app.engines.ats.section.section_parser import parse_resume_sections

from app.engines.ats.analyzers.projects.project_splitter import split_projects
from app.engines.ats.analyzers.projects.project_scoring import score_projects


def main():

    cv_path = input("CV Path: ").strip().strip('"')

    cv_text = extract_text_from_pdf(cv_path)

    cleaned = clean_resume(cv_text)

    sections = parse_resume_sections(
        cleaned["clean_text"]
    )

    projects = split_projects(
        sections.get("projects", "")
    )

    result = score_projects(projects)

    print("\n" + "=" * 80)
    print("PROJECT ANALYZER V2")
    print("=" * 80)

    print(f"\nProjects Found : {result['project_count']}")
    print(f"Average Score : {result['average_score']}")
    print(f"Total Score   : {result['total_score']}")

    for i, project in enumerate(result["projects"], start=1):

        print("\n" + "=" * 80)
        print(f"PROJECT {i}")
        print("=" * 80)

        print("Score:")
        print(project["score"])

        print("\nSkills:")
        print(project["skills"])

        print("\nAction Verbs:")
        print(project["action_verbs"])

        print("\nMetrics:")
        print(project["metrics"])

        print("\nAchievements:")
        print(project["achievements"])

        print("\nImpact:")
        print(project["impact"])

        print("\nTeamwork:")
        print(project["teamwork"])

        print("\nLinks:")
        print(project["links"])


if __name__ == "__main__":
    main()