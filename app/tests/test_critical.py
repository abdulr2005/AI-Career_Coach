import pytest

from app.engines.matching.skill_extractor import extract_skills
from app.parsers.job_parser import extract_job_skills
from app.engines.matching.match_engine import calculate_match
from app.engines.ats.ats_engine import analyze_resume
from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions
from app.engines.recommendation.resume_feedback import generate_resume_feedback


SAMPLE_CV = """
John Doe
San Francisco, CA | john@example.com | github.com/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with strong background in Python and data analysis.

WORK EXPERIENCE
Software Engineer at TechCorp (2020 - Present)
- Developed scalable microservices using Python and FastAPI
- Implemented CI/CD pipelines with Docker and Kubernetes
- Led a team of 5 engineers to deliver a machine learning platform

EDUCATION
BS Computer Science, State University (2016 - 2020)

SKILLS
Python, SQL, Docker, Kubernetes, AWS, Git, Machine Learning, Pandas

PROJECTS
ML Pipeline - Built an end-to-end machine learning pipeline using Python and TensorFlow
https://github.com/johndoe/ml-pipeline

CERTIFICATIONS
AWS Certified Solutions Architect
"""

SAMPLE_JOB = """
We are looking for a Senior Backend Engineer.

Required Skills:
Python, FastAPI, Docker, Kubernetes, AWS, SQL, PostgreSQL

Nice to have:
Machine Learning, TensorFlow, Redis
"""


class TestMatching:
    def test_extract_skills_from_cv(self):
        skills = extract_skills(SAMPLE_CV)
        assert "Python" in skills
        assert "SQL" in skills
        assert "Docker" in skills

    def test_extract_job_skills(self):
        skills = extract_job_skills(SAMPLE_JOB)
        assert "Python" in skills
        assert "FastAPI" in skills
        assert "Docker" in skills

    def test_calculate_match(self):
        cv_skills = extract_skills(SAMPLE_CV)
        job_skills = extract_job_skills(SAMPLE_JOB)
        matched, missing, score = calculate_match(cv_skills, job_skills)
        assert "Python" in matched
        assert score >= 0
        assert score <= 100


class TestATS:
    def test_analyze_resume_returns_required_fields(self):
        result = analyze_resume(SAMPLE_CV, extract_job_skills(SAMPLE_JOB))
        assert "ats_score" in result
        assert "ats_details" in result
        assert "matched_skills" in result
        assert "missing_skills" in result
        assert "match_score" in result
        assert isinstance(result["ats_score"], (int, float))
        assert 0 <= result["ats_score"] <= 100

    def test_ats_details_has_all_sub_scores(self):
        result = analyze_resume(SAMPLE_CV, extract_job_skills(SAMPLE_JOB))
        details = result["ats_details"]
        expected_keys = {
            "skill_score",
            "keyword_score",
            "section_score",
            "experience_score",
            "project_score",
            "certification_score",
            "resume_length_score",
        }
        assert expected_keys.issubset(details.keys())
        for key in expected_keys:
            assert 0 <= details[key] <= 10

    def test_analyze_resume_without_job_skills(self):
        result = analyze_resume(SAMPLE_CV)
        assert "ats_score" in result
        assert result["match_score"] == 0.0
        assert result["missing_skills"] == []


class TestRecommendations:
    def test_recommend_courses(self):
        missing = ["Machine Learning", "TensorFlow"]
        courses = recommend_courses(missing)
        assert len(courses) > 0
        assert courses[0]["skill"] == "Machine Learning"

    def test_build_roadmap(self):
        missing = ["Python", "Machine Learning"]
        roadmap = build_roadmap(missing)
        assert len(roadmap) > 0
        assert roadmap[0]["step"] == 1

    def test_generate_suggestions(self):
        suggestions = generate_suggestions(["Python"])
        assert len(suggestions) > 0
        assert "Python" in suggestions[0]

    def test_generate_resume_feedback(self):
        feedback = generate_resume_feedback(["Python"], ["Docker"])
        assert len(feedback) > 0
        assert any("matches" in f.lower() for f in feedback)


class TestCareerReportSchema:
    def test_full_pipeline_matches_schema(self):
        cv_skills = extract_skills(SAMPLE_CV)
        job_skills = extract_job_skills(SAMPLE_JOB)
        matched, missing, match_score = calculate_match(cv_skills, job_skills)
        ats_result = analyze_resume(SAMPLE_CV, job_skills)

        assert isinstance(matched, list)
        assert isinstance(missing, list)
        assert isinstance(match_score, (int, float))

        recommended = recommend_courses(missing)
        roadmap = build_roadmap(missing)
        suggestions = generate_suggestions(missing)
        feedback = generate_resume_feedback(matched, missing)

        assert "ats_score" in ats_result
        assert "ats_details" in ats_result
        assert isinstance(recommended, list)
        assert isinstance(roadmap, list)
        assert isinstance(suggestions, list)
        assert isinstance(feedback, list)
