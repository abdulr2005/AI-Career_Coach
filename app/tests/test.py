from app.parsers.pdf_reader import extract_text_from_pdf
from app.engines.skill_extractor import extract_skills
from app.parsers.job_parser import extract_job_skills
from app.engines.match_engine import calculate_match
from app.engines.course_engine import recommend_courses
from app.engines.roadmap_engine import build_roadmap


def main():

    cv_path = input("CV Path: ").strip().strip('"')

    cv_text = extract_text_from_pdf(cv_path)
    cv_skills = extract_skills(cv_text)

    print("\nPaste the Job Description (Press Enter twice to finish):")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    job_description = "\n".join(lines)

    job_skills = extract_job_skills(job_description)

    matched_skills, missing_skills, match_score = calculate_match(
        cv_skills,
        job_skills
    )

    recommended_courses = recommend_courses(missing_skills)

    roadmap = build_roadmap(missing_skills)

    print("\n========== Career Intelligence ==========\n")

    print(f"Match Score : {match_score}%")

    print("\nMatched Skills:")
    print(matched_skills)

    print("\nMissing Skills:")
    print(missing_skills)

    print("\nRecommended Courses:")

    for course in recommended_courses:
        print(f"- {course['skill']} -> {course['course']}")

    print("\nLearning Roadmap:\n")

    for step in roadmap:
        print(f"Step {step['step']}")
        print(f"Skill      : {step['skill']}")
        print(f"Difficulty : {step['difficulty']}")
        print(f"Duration   : {step['duration']}")
        print("-" * 35)


if __name__ == "__main__":
    main()