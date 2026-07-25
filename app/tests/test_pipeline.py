from app.engines.career_intelligence.pipeline import CareerPipeline

cv_text = """
Python
Machine Learning
TensorFlow
FastAPI
SQL
"""

job_description = """
We are looking for an AI Engineer.

Required Skills:
Python
FastAPI
Docker
Git
SQL
"""

pipeline = CareerPipeline()

report = pipeline.run(
    cv_text=cv_text,
    job_description=job_description
)

print("\n========== FINAL REPORT ==========\n")
print(report)