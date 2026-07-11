from app.engines.ats.section.section_matcher import match_section

tests = [
    "PROFESSIONAL SUMMARY",
    "SUMMARY",
    "TECHNICAL PROJECTS",
    "SKILLS",
    "CERTIFICATIONS",
    "EDUCATION",
]

for t in tests:
    print(f"{t}  --->  {match_section(t)}")