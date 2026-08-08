from app.data.skills_db import SKILLS_DB


def extract_job_skills(job_description):

    job_text = job_description.lower()

    extracted_skills = []

    for skill in SKILLS_DB:

        if skill.lower() in job_text:

            extracted_skills.append(skill)

    return extracted_skills
