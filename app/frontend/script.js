document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const demoModeToggle = document.getElementById('demoMode');
    const apiUrlInput = document.getElementById('apiUrl');
    const cvFileInput = document.getElementById('cvFile');
    const fileNameDisplay = document.getElementById('fileName');
    const jobDescriptionInput = document.getElementById('jobDescription');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearResultsBtn = document.getElementById('clearResults');
    const loader = document.getElementById('loader');
    const errorMsg = document.getElementById('errorMsg');
    const resultsSection = document.getElementById('resultsSection');
    const emptyState = document.getElementById('emptyState');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // State
    let analysisResult = null;

    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

    // --- Demo Data ---
    const getDemoData = () => ({
        "cv_skills": ["Python", "SQL", "Data Analysis", "Communication", "Excel"],
        "job_skills": ["Python", "SQL", "Machine Learning", "Communication", "Cloud Computing", "Leadership"],
        "matched_skills": ["Python", "SQL", "Communication"],
        "missing_skills": ["Machine Learning", "Cloud Computing", "Leadership"],
        "match_score": 68,
        "ats_score": 81,
        "ats_details": {
            "skill_score": 8.5,
            "keyword_score": 6.8,
            "section_score": 10.0,
            "experience_score": 7.2,
            "project_score": 6.5,
            "certification_score": 4.0,
            "resume_length_score": 8.0
        },
        "recommended_courses": [
            {"skill": "Machine Learning", "course": "Machine Learning Specialization", "provider": "Coursera"},
            {"skill": "Cloud Computing", "course": "AWS Cloud Practitioner Essentials", "provider": "AWS Training"},
            {"skill": "Leadership", "course": "Leading People and Teams", "provider": "University of Michigan"},
        ],
        "roadmap": [
            {"step": 1, "skill": "Machine Learning", "difficulty": "Intermediate", "duration": "4 weeks"},
            {"step": 2, "skill": "Cloud Computing", "difficulty": "Beginner", "duration": "2 weeks"},
            {"step": 3, "skill": "Leadership", "difficulty": "Advanced", "duration": "6 weeks"},
        ],
        "suggestions": [
            "Add measurable outcomes to your recent project descriptions.",
            "Highlight any cloud or ML exposure, even at a beginner level.",
            "Move your most relevant experience to the top of your resume.",
        ],
        "resume_feedback": [
            "Resume is well structured but lacks quantified achievements.",
            "Consider a concise summary section tailored to the target role.",
            "Some bullet points are too long — aim for one line each.",
        ],
    });

    // --- Initialization ---
    demoModeToggle.addEventListener('change', () => {
        apiUrlInput.disabled = demoModeToggle.checked;
    });

    cvFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            if (file.type !== 'application/pdf') {
                showError('Please upload a PDF file.');
                cvFileInput.value = '';
                fileNameDisplay.textContent = '';
                return;
            }
            if (file.size > MAX_FILE_SIZE) {
                showError('File size exceeds 10MB limit.');
                cvFileInput.value = '';
                fileNameDisplay.textContent = '';
                return;
            }
            fileNameDisplay.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        } else {
            fileNameDisplay.textContent = '';
        }
    });

    // --- Tab Logic ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });

    // --- Analysis Logic ---
    analyzeBtn.addEventListener('click', async () => {
        const isDemo = demoModeToggle.checked;
        const apiUrl = apiUrlInput.value.trim();
        const cvFile = cvFileInput.files[0];
        const jobDesc = jobDescriptionInput.value.trim();

        if (!isDemo) {
            if (!cvFile) {
                showError('Please upload a CV PDF.');
                return;
            }
            if (!jobDesc) {
                showError('Please paste a job description.');
                return;
            }
            if (!apiUrl) {
                showError('Please enter a backend endpoint URL.');
                return;
            }
        }

        hideError();
        loader.style.display = 'block';
        analyzeBtn.disabled = true;

        try {
            if (isDemo) {
                await new Promise(resolve => setTimeout(resolve, 1200));
                renderResults(getDemoData());
            } else {
                const data = await fetchWithRetry(apiUrl, cvFile, jobDesc);
                renderResults(data);
            }
        } catch (err) {
            showError(getUserFriendlyError(err));
            emptyState.style.display = 'block';
            resultsSection.style.display = 'none';
        } finally {
            loader.style.display = 'none';
            analyzeBtn.disabled = false;
        }
    });

    clearResultsBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        emptyState.style.display = 'block';
        clearResultsBtn.style.display = 'none';
        analysisResult = null;
    });

    // --- Network ---
    async function fetchWithRetry(url, file, jobDesc, retries = 2) {
        for (let attempt = 0; attempt <= retries; attempt++) {
            try {
                return await fetchWithTimeout(url, file, jobDesc);
            } catch (err) {
                if (attempt === retries) throw err;
                await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
            }
        }
    }

    function fetchWithTimeout(url, file, jobDesc, timeout = 60000) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_description', jobDesc);

        return fetch(url, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        }).then(async (response) => {
            clearTimeout(timeoutId);
            if (!response.ok) {
                let errorText = '';
                try {
                    const errJson = await response.json();
                    errorText = errJson.detail || JSON.stringify(errJson);
                } catch {
                    errorText = await response.text();
                }
                throw new Error(`Server error (${response.status}): ${errorText}`);
            }
            return response.json();
        }).catch(err => {
            clearTimeout(timeoutId);
            if (err.name === 'AbortError') {
                throw new Error('Request timed out. The backend is taking too long to respond.');
            }
            throw err;
        });
    }

    // --- Rendering ---
    function renderResults(data) {
        analysisResult = data;
        resultsSection.style.display = 'block';
        clearResultsBtn.style.display = 'block';

        // Overview
        const matchScore = Number(data.match_score) || 0;
        const atsScore = Number(data.ats_score) || 0;

        document.getElementById('matchScoreVal').textContent = `${Math.round(matchScore)}%`;
        setProgressColor('matchScoreFill', matchScore);
        document.getElementById('matchScoreFill').style.width = `${Math.min(matchScore, 100)}%`;
        
        document.getElementById('atsScoreVal').textContent = `${Math.round(atsScore)}%`;
        setProgressColor('atsScoreFill', atsScore);
        document.getElementById('atsScoreFill').style.width = `${Math.min(atsScore, 100)}%`;
        
        document.getElementById('matchedSkillsCount').textContent = (data.matched_skills || []).length;
        document.getElementById('missingSkillsCount').textContent = (data.missing_skills || []).length;

        // Skills Tags
        renderTags('matchedSkillsTags', data.matched_skills, 'tag-good');
        renderTags('missingSkillsTags', data.missing_skills, 'tag-bad');

        // All Skills Lists
        renderList('cvSkillsList', data.cv_skills);
        renderList('jobSkillsList', data.job_skills);

        // ATS Details
        renderAtsDetails(data.ats_details);

        // Recommended Courses
        const coursesGrid = document.getElementById('coursesGrid');
        coursesGrid.innerHTML = '';
        if (data.recommended_courses && data.recommended_courses.length > 0) {
            data.recommended_courses.forEach(course => {
                const card = document.createElement('div');
                card.className = 'course-card';
                card.innerHTML = `
                    <h4>${course.course || 'Untitled Course'}</h4>
                    <p class="provider">${course.provider || 'Unknown Provider'}</p>
                    <p>Builds: <strong>${course.skill || 'N/A'}</strong></p>
                `;
                coursesGrid.appendChild(card);
            });
        } else {
            coursesGrid.innerHTML = '<p class="help-text">No course recommendations available.</p>';
        }

        // Roadmap
        const roadmapList = document.getElementById('roadmapList');
        roadmapList.innerHTML = '';
        if (data.roadmap && data.roadmap.length > 0) {
            const sortedRoadmap = [...data.roadmap].sort((a, b) => (a.step || 0) - (b.step || 0));
            sortedRoadmap.forEach((item, idx) => {
                const stepNum = item.step || (idx + 1);
                const difficultyClass = `badge-${(item.difficulty || 'beginner').toLowerCase()}`;
                const roadmapItem = document.createElement('div');
                roadmapItem.className = 'roadmap-item';
                roadmapItem.innerHTML = `
                    <div class="roadmap-info">
                        <h4>Step ${stepNum}: ${item.skill}</h4>
                        <p class="help-text">Estimated duration: ${item.duration || 'Unspecified'}</p>
                    </div>
                    <div class="roadmap-meta">
                        <span class="badge ${difficultyClass}">${item.difficulty || 'Beginner'}</span>
                    </div>
                `;
                roadmapList.appendChild(roadmapItem);
            });
        } else {
            roadmapList.innerHTML = '<p class="help-text">No roadmap available.</p>';
        }

        // Lists (Feedback & Suggestions)
        renderBulletList('feedbackList', data.resume_feedback);
        renderBulletList('suggestionsList', data.suggestions);
    }

    function renderAtsDetails(details) {
        const section = document.getElementById('atsDetailsSection');
        const grid = document.getElementById('atsDetailsGrid');
        grid.innerHTML = '';

        if (!details) {
            section.style.display = 'none';
            return;
        }

        const items = [
            { label: 'Skill score', value: details.skill_score },
            { label: 'Keyword score', value: details.keyword_score },
            { label: 'Section score', value: details.section_score },
            { label: 'Experience score', value: details.experience_score },
            { label: 'Project score', value: details.project_score },
            { label: 'Certification score', value: details.certification_score },
            { label: 'Resume length score', value: details.resume_length_score },
        ];

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'ats-detail-card';
            const score = Number(item.value) || 0;
            const colorClass = getScoreColorClass(score);
            card.innerHTML = `
                <span class="ats-detail-label">${item.label}</span>
                <span class="ats-detail-value ${colorClass}">${score.toFixed(1)}</span>
            `;
            grid.appendChild(card);
        });

        section.style.display = 'block';
    }

    function setProgressColor(elementId, score) {
        const el = document.getElementById(elementId);
        const numScore = Number(score) || 0;
        if (numScore >= 80) {
            el.style.backgroundColor = '#28a745';
        } else if (numScore >= 60) {
            el.style.backgroundColor = '#ffc107';
        } else {
            el.style.backgroundColor = '#dc3545';
        }
    }

    function getScoreColorClass(score) {
        if (score >= 8) return 'score-high';
        if (score >= 6) return 'score-medium';
        return 'score-low';
    }

    function renderTags(containerId, items, className) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        if (items && items.length > 0) {
            items.forEach(item => {
                const span = document.createElement('span');
                span.className = `tag ${className}`;
                span.textContent = item;
                container.appendChild(span);
            });
        } else {
            container.innerHTML = '<span class="help-text">None</span>';
        }
    }

    function renderList(containerId, items) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        if (items && items.length > 0) {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                container.appendChild(li);
            });
        } else {
            container.innerHTML = '<li>No skills found.</li>';
        }
    }

    function renderBulletList(containerId, items) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        if (items && items.length > 0) {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                container.appendChild(li);
            });
        } else {
            container.innerHTML = '<li class="help-text">Nothing to show yet.</li>';
        }
    }

    function getUserFriendlyError(err) {
        const msg = err.message || 'An unknown error occurred.';
        if (msg.includes('Failed to fetch') || msg.includes('NetworkError')) {
            return 'Cannot reach the backend. Please check the endpoint URL and ensure the server is running.';
        }
        if (msg.includes('timeout') || msg.includes('timed out')) {
            return 'The request timed out. Please try again.';
        }
        if (msg.includes('400')) {
            return 'Invalid request. Please check your inputs and try again.';
        }
        if (msg.includes('413')) {
            return 'The uploaded file is too large. Please use a file under 10MB.';
        }
        if (msg.includes('415')) {
            return 'Unsupported file type. Please upload a PDF.';
        }
        if (msg.includes('500')) {
            return 'The server encountered an error. Please try again later.';
        }
        return msg;
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.style.display = 'block';
    }

    function hideError() {
        errorMsg.style.display = 'none';
        errorMsg.textContent = '';
    }
});
