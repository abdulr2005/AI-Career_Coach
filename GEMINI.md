# GEMINI.md — AI Career Coach Project Instructions

## 1. Project Mission

You are working on an **AI Career Coach** application.

The core user flow is:

1. The user enters/pastes a **job description**.
2. The user uploads their **CV/resume as a PDF**.
3. The backend parses both inputs.
4. The system compares the CV against the job description.
5. The backend generates a career-analysis report containing:
   - skill match score
   - missing skills / skill gaps
   - ATS score
   - ATS details/sub-scores
   - recommended courses
   - learning roadmap
   - resume feedback
   - actionable suggestions
6. The frontend displays the complete report clearly.

The project currently uses:

- **Backend:** Python + FastAPI
- **Frontend:** vanilla HTML/CSS/JavaScript
- **PDF parsing:** existing PDF reader/parser code
- **Fuzzy matching:** RapidFuzz
- **Validation/schema:** Pydantic

Do not change the project into a different framework unless explicitly requested.

---

# 2. PRIMARY OBJECTIVE

Your job is to make the existing codebase **actually work end-to-end**.

Do not merely patch individual errors.

Trace the complete flow:

```text
Job Description
      +
    CV PDF
      ↓
API request
      ↓
PDF extraction / resume parsing
      ↓
Job parsing
      ↓
Skill extraction
      ↓
Skill matching
      ↓
ATS analysis
      ↓
Career intelligence
      ↓
Recommendations / roadmap / resume feedback
      ↓
Validated response schema
      ↓
Frontend rendering
```

The final implementation must allow a real user to upload a CV and submit a job description and receive a valid report without runtime errors.

---

# 3. IMPORTANT WORKING RULES

## 3.1 Inspect before editing

Before changing code:

- inspect the actual repository
- inspect imports
- inspect function signatures
- inspect Pydantic models
- inspect API routes
- inspect frontend JavaScript
- inspect all modules involved in the career-report flow
- inspect existing tests

The `CURRENT.md` document describes known problems, but it is a **diagnostic snapshot**, not a substitute for inspecting the actual source files.

Do not assume that every issue in `CURRENT.md` is still present.

Do not invent files, functions, return values, or APIs without checking the repository.

---

## 3.2 Preserve working functionality

Fix the existing implementation instead of rewriting the whole application unnecessarily.

Prefer:

- small, coherent changes
- reuse of existing engines
- existing schemas
- existing parsing logic
- existing matching logic
- existing recommendation logic

Avoid introducing unnecessary frameworks or dependencies.

---

## 3.3 Do not hide errors

Never solve a problem by:

- swallowing exceptions
- returning fake data
- hardcoding successful API responses
- bypassing broken modules
- disabling tests
- commenting out failing functionality
- returning empty results just to make the frontend render

If something is genuinely unavailable, implement the smallest correct fallback and document it.

---

# 4. KNOWN CODEBASE PROBLEMS

The current project-state document identifies the following important problems.

## Critical backend bugs

### BUG-001 — `analyze_resume` signature mismatch

The current ATS function is described as accepting:

```python
analyze_resume(cv_skills, job_skills)
```

while the API route calls it with:

```python
analyze_resume(cv_text)
```

Resolve this architecturally.

Preferred design:

```text
calculate_skill_match(cv_skills, job_skills)
        ↓
analyze_resume(cv_text, job_description / parsed data)
        ↓
complete ATS analysis
```

Do not overload one function with incompatible responsibilities.

---

### BUG-002 — ATS return-value mismatch

The route expects dictionary-style data such as:

```python
ats_result["ats_score"]
ats_result["details"]
```

while the existing skill-matching implementation returns a tuple similar to:

```python
(matched_skills, missing_skills, match_score)
```

Create a clear internal result structure.

The API should receive one predictable ATS result object/dictionary with explicit fields.

Prefer typed models where practical.

---

### BUG-003 — ATS engine is incomplete

The ATS engine must actually orchestrate the existing ATS components where appropriate:

- resume cleaning
- section parsing
- section matching
- skill analysis
- experience analysis
- project analysis
- certification analysis
- ATS scoring
- resume scoring
- report/summary generation

Do not call a simple skill matcher an "ATS engine" if the application promises a full ATS analysis.

---

### BUG-004 — duplicate `clean_resume`

Remove duplicate definitions and keep one canonical implementation.

---

# 5. ARCHITECTURE REQUIREMENTS

Keep responsibilities separated.

Recommended conceptual architecture:

```text
app/
├── api/
│   └── routes.py
│
├── models/
│   └── schemas.py
│
├── parsers/
│   ├── pdf_reader.py
│   ├── resume_parser.py
│   └── job_parser.py
│
├── engines/
│   ├── ats/
│   ├── matching/
│   ├── career_intelligence/
│   └── recommendation/
│
├── data/
│   ├── ats_db.py
│   ├── skills_db.py
│   ├── resume_patterns.py
│   ├── project_patterns.py
│   ├── courses_db.py
│   └── roadmap_db.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── main.py
```

Do not move files around unless doing so solves a real architectural problem.

---

# 6. SINGLE SOURCE OF TRUTH

There are currently duplicated skill/keyword/pattern definitions.

Examples include:

- `data/skills_db.py`
- ATS skill extractor keywords
- experience technical keywords
- project technical keywords
- resume section patterns
- parser section patterns

Consolidate duplicated constants where practical.

There should be one authoritative source for each category.

For example:

```text
skills → data/skills_db.py
resume sections → data/resume_patterns.py
project language/patterns → data/project_patterns.py
ATS configuration → data/ats_db.py
courses → data/courses_db.py
roadmaps → data/roadmap_db.py
```

Do not create circular imports while doing this.

---

# 7. ATS RESULT CONTRACT

The ATS engine must expose a stable result contract.

At minimum, the result must support:

```text
ats_score
ats_details
```

`ats_details` must contain the ATS sub-scores expected by the existing `CareerReportResponse`.

Also preserve:

```text
matched_skills
missing_skills
match_score
```

if they are part of the public career report.

The exact fields and types must be taken from the actual `app/models/schemas.py`.

Do not invent a conflicting response schema.

---

# 8. API CONTRACT

The primary endpoint is the career-report flow.

It should accept:

```text
job_description
cv PDF
```

The implementation must:

1. validate the uploaded file
2. extract CV text
3. reject invalid/empty CVs
4. validate the job description
5. parse/extract relevant job skills
6. analyze the CV
7. calculate matching
8. calculate ATS results
9. generate recommendations
10. generate roadmap
11. generate resume feedback
12. return the exact response defined by the Pydantic response model

Use FastAPI `HTTPException` for expected client errors.

Do not expose stack traces to users.

---

# 9. FRONTEND CONTRACT

The frontend must consume exactly the backend response schema.

Do not maintain a second unofficial API contract in JavaScript.

`renderResults()` must render all important response fields, including:

- match score
- ATS score
- ATS details
- matched skills
- missing skills
- recommended courses
- roadmap
- suggestions
- resume feedback

If a field is optional, render an appropriate empty state rather than crashing.

---

# 10. FRONTEND REQUIREMENTS

Fix the known frontend problems.

## File validation

Before uploading:

- require a file
- require PDF
- enforce a reasonable size limit
- show a clear validation message

The backend must repeat these validations. Never rely only on frontend validation.

---

## Request timeout

Use `AbortController`.

The frontend must not wait indefinitely for a broken backend.

---

## Retry

Implement limited retry behavior for transient failures.

Do not retry validation errors such as:

- invalid PDF
- missing job description
- malformed request

---

## Error handling

Never display raw stack traces or internal exceptions.

Convert API errors into user-friendly messages.

---

## Loading state

Show a clear analysis state without destroying useful previous results unnecessarily.

---

## Score visualization

Score bars should communicate quality.

A reasonable interpretation:

```text
80–100 → high
60–79  → medium
0–59   → low
```

Keep the implementation consistent across match and ATS scores.

---

## Accessibility

Improve the frontend with:

- labels
- semantic elements
- appropriate ARIA attributes where necessary
- keyboard-friendly controls
- meaningful button text
- accessible error/status messages

---

# 11. FASTAPI APPLICATION

Fix route conflicts.

There must be one clear frontend/root route.

Avoid having both:

```python
router.get("/")
app.get("/")
```

serve competing content.

Keep API routes clearly separated from frontend/static routes.

Prefer an API namespace such as:

```text
/api/...
```

if this can be introduced without breaking the existing project.

Add:

```text
GET /health
```

returning:

```json
{"status": "ok"}
```

---

# 12. CORS

If frontend and backend run on different origins during development, configure CORS correctly.

Development can use permissive origins if necessary, but production configuration should use explicit allowed origins.

Do not use:

```python
allow_origins=["*"]
```

together with credentialed requests as a production security solution.

---

# 13. FILE UPLOAD SAFETY

The CV upload must have backend validation.

At minimum:

- PDF extension validation
- MIME/content validation where practical
- maximum file size
- reject empty files
- reject PDFs from which no meaningful text can be extracted
- avoid storing uploaded files permanently unless storage is intentionally implemented

Do not trust only the browser-provided MIME type.

---

# 14. LOGGING

Replace debugging `print()` statements in backend code with Python logging.

Use appropriate levels:

```text
DEBUG
INFO
WARNING
ERROR
```

Do not log:

- complete CV contents
- sensitive user data
- secrets
- authentication tokens

Logs should help diagnose API and pipeline failures without leaking user documents.

---

# 15. DEPENDENCIES

Create a dependency file if one does not exist.

Prefer:

```text
requirements.txt
```

unless the repository already uses another dependency-management system.

Only include packages actually used by the project.

Do not add libraries merely because they might be useful.

---

# 16. TESTS

Fix broken imports in existing tests.

Then test the real pipeline.

At minimum, tests should cover:

### Matching

```text
CV skills + job skills
→ matched skills
→ missing skills
→ match score
```

### PDF parsing

```text
PDF
→ extracted text
```

### ATS

```text
CV text
→ ATS result
→ valid ats_score
→ valid ats_details
```

### Career report

```text
job description + CV
→ CareerReportResponse-compatible result
```

### API

Test:

- valid request
- missing job description
- missing file
- invalid file
- empty extracted CV
- successful report

Do not weaken tests to match broken implementation.

---

# 17. DATA / RECOMMENDATION ENGINES

The project has course and roadmap engines.

Keep the existing behavior where possible.

If `courses_db.py` or `roadmap_db.py` is empty but corresponding engines contain hardcoded data, decide on one source of truth and move the data into the intended data modules.

The output should be deterministic and explainable.

Recommendations should be based on missing skills rather than arbitrary suggestions.

---

# 18. CAREER INTELLIGENCE

The career intelligence layer should sit above low-level parsing/matching.

Conceptually:

```text
Raw CV
  ↓
Parsed CV
  ↓
Job requirements
  ↓
Skill match + ATS analysis
  ↓
Career intelligence
  ↓
Recommendations
```

Do not duplicate skill extraction logic inside career intelligence.

If `career_intelligence/analyzer.py` is referenced but missing, inspect actual imports first.

Then either:

- implement the missing module if the architecture requires it, or
- remove stale references if it is no longer needed.

Do not create an unused placeholder just to satisfy a tree/document.

---

# 19. ERROR HANDLING

Expected user errors should produce useful HTTP responses.

Examples:

```text
400 — invalid input
413 — file too large
415 — unsupported file type
422 — validation failure
500 — unexpected server error
```

Do not expose internal implementation details in production responses.

Keep useful technical details in logs.

---

# 20. CODE QUALITY

While fixing the project:

- use clear function names
- avoid duplicate functions
- avoid circular imports
- avoid unnecessary global mutable state
- avoid hidden side effects
- use type hints where useful
- keep functions focused
- keep API route handlers thin
- put business logic in engines/services
- keep schemas in `models/`
- keep parsing in `parsers/`

Do not perform a massive style rewrite unrelated to functionality.

---

# 21. WHAT NOT TO DO

Do NOT:

- replace FastAPI with Flask
- replace vanilla JS with React
- introduce a database just for the sake of it
- introduce an LLM API just because the project is called AI Career Coach
- fabricate course recommendations
- fabricate ATS scores
- hardcode a successful analysis
- remove existing features to make tests pass
- silently ignore failing modules
- change the public API without updating both backend and frontend
- create duplicate implementations of existing engines

The first goal is a reliable deterministic MVP.

AI/LLM functionality can be added later if explicitly requested.

---

# 22. IMPLEMENTATION ORDER

Follow this order.

## Phase 1 — Understand

Inspect:

```text
app/main.py
app/api/routes.py
app/models/schemas.py
app/parsers/*
app/engines/ats/*
app/engines/matching/*
app/engines/career_intelligence/*
app/engines/recommendation/*
app/frontend/*
app/tests/*
```

Trace the career-report request from frontend to response.

---

## Phase 2 — Fix imports and structural failures

Fix:

- invalid imports
- missing modules
- duplicate definitions
- filename/import mismatches
- circular imports
- stale references

---

## Phase 3 — Fix ATS pipeline

Make one coherent pipeline:

```text
CV
 ↓
clean
 ↓
parse sections
 ↓
extract information
 ↓
analyze skills
 ↓
analyze experience/projects/certifications
 ↓
score
 ↓
build ATS result
```

---

## Phase 4 — Fix API

Make the endpoint call the pipeline correctly.

Ensure the response exactly matches the Pydantic response schema.

---

## Phase 5 — Fix frontend

Make frontend request and response handling match the backend.

Render every important report field.

---

## Phase 6 — Validation and error handling

Add:

- upload validation
- input validation
- timeout
- friendly errors
- CORS
- health endpoint
- logging

---

## Phase 7 — Tests

Run the existing tests.

Fix the implementation, not the tests, when behavior is supposed to be correct.

Add missing tests for the complete report pipeline.

---

## Phase 8 — Final verification

Run:

```text
pytest
```

and start the application.

Then manually verify:

```text
GET /health
```

and the complete browser flow:

```text
enter job description
→ upload CV PDF
→ Analyze
→ wait
→ report appears
```

There must be no backend traceback and no frontend JavaScript error for the normal successful flow.

---

# 23. DEFINITION OF DONE

The task is complete only when all of the following are true:

- [ ] Project imports successfully
- [ ] FastAPI starts successfully
- [ ] `/health` works
- [ ] frontend loads
- [ ] frontend can submit a job description
- [ ] frontend can upload a PDF CV
- [ ] backend extracts CV text
- [ ] job skills are extracted
- [ ] CV skills are extracted
- [ ] matching works
- [ ] ATS analysis works
- [ ] ATS details are returned
- [ ] career report is generated
- [ ] recommendations work
- [ ] roadmap works
- [ ] resume feedback works
- [ ] frontend renders the complete report
- [ ] invalid input produces friendly errors
- [ ] oversized/invalid uploads are rejected
- [ ] no raw traceback is shown to the user
- [ ] existing tests pass
- [ ] new critical-path tests pass
- [ ] no obvious duplicate implementations remain
- [ ] no broken imports remain
- [ ] no debug `print()` calls remain in production backend code

---

# 24. FINAL REPORT AFTER MAKING CHANGES

After implementing fixes, report:

1. What you changed.
2. Which known problems from `CURRENT.md` were fixed.
3. Which files were modified/created.
4. Tests executed and their results.
5. Any remaining problems.
6. Any assumptions made because the repository did not provide enough information.

Do not claim a test or command passed unless you actually ran it.

