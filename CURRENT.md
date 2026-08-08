# AI Career Coach - Current Codebase State

## 1. Project Overview

This is an AI-powered career coaching platform built with FastAPI (backend) and vanilla HTML/CSS/JS (frontend). The system analyzes a user's CV against a job description to provide skill gap analysis, ATS scoring, course recommendations, learning roadmaps, and resume feedback.

## 2. Directory Structure

```
app/
├── main.py                    # FastAPI app entry point
├── __init__.py
├── api/
│   ├── __init__.py
│   └── routes.py              # API endpoints
├── data/
│   ├── __init__.py
│   ├── ats_db.py              # ATS weights and keywords
│   ├── courses_db.py          # EMPTY
│   ├── project_patterns.py    # Action verbs, impact words, etc.
│   ├── resume_patterns.py     # Section detection patterns
│   ├── roadmap_db.py          # EMPTY
│   └── skills_db.py           # Static skill list (28 items)
├── database/
│   └── __init__.py            # EMPTY
├── docs/                      # Documentation
├── engines/
│   ├── __init__.py
│   ├── ats/
│   │   ├── __init__.py
│   │   ├── ats_engine.py      # ATS orchestrator
│   │   ├── analyzers/
│   │   │   ├── certifications/
│   │   │   ├── experience/
│   │   │   ├── projects/
│   │   │   └── skills/
│   │   ├── report/
│   │   │   ├── report_builder.py
│   │   │   ├── score_builder.py
│   │   │   └── summary_builder.py
│   │   ├── scoring/
│   │   │   ├── ats/
│   │   │   ├── resume/
│   │   │   └── skills/
│   │   └── section/
│   │       ├── normalizer.py      # NOTE: filename has typo "\normalizer.py"
│   │       ├── resume_cleaner.py
│   │       ├── section_matcher.py
│   │       ├── section_parser.py
│   │       └── section_utils.py
│   ├── career_intelligence/
│   │   ├── __init__.py
│   │   ├── analyzer.py        # MISSING FILE
│   │   ├── models.py
│   │   ├── pipeline.py
│   │   ├── recommendation_engine.py
│   │   └── report_generator.py
│   ├── matching/
│   │   ├── match_engine.py
│   │   └── skill_extractor.py
│   └── recommendation/
│       ├── course_engine.py
│       ├── resume_feedback.py
│       ├── roadmap_engine.py
│       └── suggestion_engine.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic request/response models
├── parsers/
│   ├── __init__.py
│   ├── job_parser.py
│   ├── pdf_reader.py
│   └── resume_parser.py       # Duplicates data/resume_patterns.py
├── services/
│   └── __init__.py            # EMPTY
├── tests/
│   ├── test.py                # BROKEN IMPORTS
│   ├── test_matcher.py
│   ├── test_project_scoring.py
│   ├── test_project_splitter.py
│   └── test_pipeline.py
└── utils/
    └── __init__.py            # EMPTY
```

---

## 3. Backend Problems

### 3.1 Critical Runtime Bugs

**BUG-001: `analyze_resume` function signature mismatch**
- **File**: `app/engines/ats/ats_engine.py:28` and `app/api/routes.py:152`
- **Problem**: `analyze_resume(cv_skills, job_skills)` is defined to take two list arguments, but in `routes.py` it is called as `analyze_resume(cv_text)` with a single string argument. This will raise a `TypeError` at runtime.

**BUG-002: Return value access mismatch**
- **File**: `app/api/routes.py:160-213`
- **Problem**: `analyze_resume()` returns a tuple `(matched_skills, missing_skills, match_score)`, but the code accesses it as a dict: `ats_result["ats_score"]` and `ats_result["details"]`. This will raise a `TypeError`.

**BUG-003: ATS engine does not perform ATS analysis**
- **File**: `app/engines/ats/ats_engine.py`
- **Problem**: Despite its name, this function only performs skill matching. It does not call section parser, experience analyzer, project scorer, or certification analyzer. The `score_builder.py` and `summary_builder.py` exist but are never called by `ats_engine.py`.

**BUG-004: Duplicate function definition**
- **File**: `app/engines/ats/section/resume_cleaner.py:165-186`
- **Problem**: `clean_resume()` is defined twice in the same file (lines 172-186 and the docstring block at 165-169 is also duplicated).

### 3.2 Structural Issues

**ISS-001: Empty database/services modules**
- `app/database/__init__.py` and `app/services/__init__.py` are completely empty. No database connection, no service layer abstraction.

**ISS-002: Empty data files**
- `app/data/courses_db.py` and `app/data/roadmap_db.py` are empty, yet `course_engine.py` and `roadmap_engine.py` contain hardcoded dictionaries.

**ISS-003: Duplicated keyword/skill databases**
- `SKILLS_DB` in `data/skills_db.py`
- `SKILL_KEYWORDS` in `engines/ats/analyzers/skills/skill_extractor.py`
- `TECH_KEYWORDS` in `engines/ats/analyzers/experience/experience.py`
- `TECH_KEYWORDS` in `engines/ats/analyzers/projects/projects.py`
- `SECTION_PATTERNS` in both `data/resume_patterns.py` and `parsers/resume_parser.py`

**ISS-004: Filename typo**
- `app/engines/ats/section/\normalizer.py` - The filename contains a backslash character.

**ISS-005: Missing file**
- `app/engines/career_intelligence/analyzer.py` is referenced in `project_tree.txt` but does not exist.

**ISS-006: Unused Pydantic schema**
- `CareerRequest` model in `models/schemas.py` is defined but never used. The `/career-report` endpoint manually extracts `file` and `job_description` from Form/File instead of using the schema.

**ISS-007: Print statements in production code**
- `section_parser.py:29-35` contains `print()` statements that will clutter logs.

### 3.3 Missing Backend Infrastructure

**MISS-001: No authentication/users**
- The backend docs explicitly list authentication and users as responsibilities, but nothing exists.

**MISS-002: No file storage**
- Uploaded PDFs are read into memory and discarded. No persistent storage.

**MISS-003: No error handling middleware**
- `routes.py:119` raises a raw `ValueError` instead of `HTTPException`.

**MISS-004: No CORS configuration**
- Frontend running on a different origin will be blocked.

**MISS-005: No requirements.txt / pyproject.toml**
- No dependency management file found at project root.

**MISS-006: No logging configuration**
- Uses `print()` instead of structured logging.

**MISS-007: No input validation/sanitization**
- File uploads have no size limits or content validation beyond text extraction.

### 3.4 Broken Tests

**TEST-001: Wrong imports in test.py**
- `app/tests/test.py` imports from non-existent paths:
  - `from app.engines.skill_extractor import extract_skills` (should be `app.engines.matching.skill_extractor`)
  - `from app.engines.match_engine import calculate_match` (should be `app.engines.matching.match_engine`)
  - `from app.engines.course_engine import recommend_courses` (should be `app.engines.recommendation.course_engine`)
  - `from app.engines.roadmap_engine import build_roadmap` (should be `app.engines.recommendation.roadmap_engine`)

---

## 4. Frontend Problems

### 4.1 Functional Issues

**ISS-F001: Hardcoded API URL**
- **File**: `app/frontend/index.html:29`
- **Problem**: `apiUrl` input is `disabled` with value `http://localhost:8000/career-report`. Users cannot change it.

**ISS-F002: Missing `ats_details` rendering**
- The backend `CareerReportResponse` includes `ats_details` (with 8 sub-fields), but the frontend does not render this data anywhere.

**ISS-F003: Demo data does not match API response**
- The demo data includes `resume_feedback` which is correct, but does not include `ats_details` which the API now requires in the schema.

**ISS-F004: No timeout handling**
- The `fetch()` call in `script.js:105` has no timeout. A slow backend will block the UI indefinitely.

**ISS-F005: Minimal file validation**
- The frontend only checks if a file is selected. It does not validate MIME type, file size, or actual PDF content.

### 4.2 UX Issues

**ISS-F006: Full-page loading block**
- During analysis, the entire results area is hidden with a spinner. Users cannot see previous results or interact with other parts of the page.

**ISS-F007: No retry logic**
- If the API request fails, the user must manually click "Analyze" again.

**ISS-F008: Raw error messages**
- `script.js:119` shows raw error text to users, which may contain stack traces or internal details.

**ISS-F009: Progress bar color is static**
- All progress bars use the same blue color regardless of score quality (e.g., 30% and 90% both look identical).

**ISS-F010: No accessibility attributes**
- Missing ARIA labels, keyboard navigation hints, and semantic HTML enhancements.

---

## 5. Frontend-Backend Linking Problems

### 5.1 Route Conflicts

**LINK-001: Duplicate root route**
- `app/main.py` defines both `router.get("/")` (returns JSON) and `app.get("/")` (returns `index.html`). These will conflict.

**LINK-002: Static file mount intercepts API**
- `app/main.py:23` mounts `StaticFiles` at `/`. While FastAPI checks router routes first, any typo in API paths will silently return a 404 from the static file handler instead of a proper API 404.

### 5.2 Response Schema Mismatch

**LINK-003: Frontend expects fields backend doesn't provide**
- The frontend `renderResults()` expects `match_score`, `ats_score`, `matched_skills`, `missing_skills`, `recommended_courses`, `roadmap`, `suggestions`, `resume_feedback`.
- The backend `CareerReportResponse` schema includes all of these, BUT the actual implementation is broken (BUG-001, BUG-002), so the API currently cannot produce a valid response.

**LINK-004: Missing `ats_details` in frontend**
- Backend returns `ats_details: ATSDetails` but frontend does not render it.

### 5.3 Data Flow Issues

**LINK-005: No CORS**
- Frontend runs on a static file server or different port. Without CORS middleware, `fetch()` will fail with a CORS error.

**LINK-006: No request/response logging**
- Backend does not log incoming requests or outgoing responses, making debugging the frontend-backend integration difficult.

---

## 6. Suggested Fixes

### 6.1 Immediate Critical Fixes (Backend)

1. **Fix `analyze_resume` signature and implementation**
   - Either change the function to accept `cv_text` and perform full ATS analysis (section parsing, skill extraction, experience analysis, project scoring, certification analysis, score building, summary building), or rename the existing function to `calculate_skill_match` and create a proper `analyze_resume(cv_text)` wrapper.

2. **Fix `routes.py` response construction**
   - Replace `ats_result["ats_score"]` and `ats_result["details"]` with actual computed values from the ATS engine.
   - Ensure `ats_result` is a dict with the expected keys.

3. **Remove duplicate `clean_resume` definition**
   - Keep only one definition in `resume_cleaner.py`.

4. **Fix `score_builder.py` and `summary_builder.py`**
   - Change `certifications.get("count", 0)` to `certifications.get("total_certifications", 0)` to match the actual return value from `analyze_certifications`.

5. **Add proper error handling**
   - Replace `raise ValueError(...)` with `from fastapi import HTTPException; raise HTTPException(status_code=400, detail="...")`.

6. **Fix `main.py` route conflicts**
   - Remove `router.get("/")` or change `app.get("/")` to serve a different path.
   - Ensure `StaticFiles` mount does not intercept API routes.

### 6.2 Backend Architecture Fixes

7. **Unify skill/keyword databases**
   - Create a single source of truth for skills, keywords, and section patterns.
   - Import from `data/` in all other modules.

8. **Fix filename typo**
   - Rename `app/engines/ats/section/\normalizer.py` to `normalizer.py` and update all imports.

9. **Create missing `analyzer.py`**
   - Either create the file or remove the reference from `project_tree.txt`.

10. **Add CORS middleware**
    - `from fastapi.middleware.cors import CORSMiddleware` with appropriate origins.

11. **Add `requirements.txt`**
    - List all dependencies: `fastapi`, `uvicorn`, `pdfplumber`, `pydantic`, `rapidfuzz`, etc.

12. **Replace print statements with logging**
    - Use Python's `logging` module throughout the codebase.

### 6.3 Frontend Fixes

13. **Enable API URL editing**
    - Remove `disabled` attribute from `apiUrl` input or provide a settings mechanism.

14. **Render `ats_details`**
    - Add a new section in the UI to display the 8 ATS sub-scores.

15. **Update demo data**
    - Include `ats_details` in the demo data object.

16. **Add request timeout**
    - Use `AbortController` with `fetch()` to implement a 30-60 second timeout.

17. **Improve file validation**
    - Check file.type === 'application/pdf' and add a size limit (e.g., 10MB).

18. **Add retry logic**
    - Implement 1-2 retries with exponential backoff for transient failures.

19. **Improve error messages**
    - Parse error responses and show user-friendly messages.

20. **Dynamic progress bar colors**
    - Use green for high scores, yellow for medium, red for low.

### 6.4 Integration Fixes

21. **Add CORS to FastAPI**
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```

22. **Align response schema**
    - Ensure backend `CareerReportResponse` and frontend `renderResults()` agree on all field names and types.

23. **Add health check endpoint**
    - `GET /health` returning `{"status": "ok"}` for frontend connectivity checks.

24. **Fix test imports**
    - Update `app/tests/test.py` with correct import paths.

### 6.5 Long-term Improvements

25. **Add database layer**
    - Use SQLAlchemy or similar for user data, analysis history, and file metadata.

26. **Add authentication**
    - JWT or session-based auth to protect user data.

27. **Add request validation**
    - Validate PDF content type and size in the route handler.

28. **Add rate limiting**
    - Prevent abuse of the analysis endpoint.

29. **Add response caching**
    - Cache job description analysis results to improve performance.

30. **Add unit tests for ATS engine**
    - The current tests only cover project splitting and matching. ATS analysis is untested.
