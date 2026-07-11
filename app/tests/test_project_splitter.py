from app.parsers.pdf_reader import extract_text_from_pdf

from app.engines.ats.section.resume_cleaner import clean_resume
from app.engines.ats.section.section_parser import parse_resume_sections

from app.engines.ats.analyzers.project_splitter import split_projects


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

    print("\n" + "=" * 70)
    print("PROJECT SPLITTER TEST")
    print("=" * 70)

    print(f"\nDetected Projects: {len(projects)}\n")

    for i, project in enumerate(projects, start=1):

        print("=" * 70)
        print(f"PROJECT {i}")
        print("=" * 70)
        print(project[:500])
        print()


if __name__ == "__main__":
    main()