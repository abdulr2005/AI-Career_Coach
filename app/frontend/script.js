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

    // --- Demo Data ---
    const getDemoData = () => ({
        "cv_skills": ["Python", "SQL", "Data Analysis", "Communication", "Excel"],
        "job_skills": ["Python", "SQL", "Machine Learning", "Communication", "Cloud Computing", "Leadership"],
        "matched_skills": ["Python", "SQL", "Communication"],
        "missing_skills": ["Machine Learning", "Cloud Computing", "Leadership"],
        "match_score": 68,
        "ats_score": 81,
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
            fileNameDisplay.textContent = `Selected: ${file.name}`;
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
        const apiUrl = apiUrlInput.value;
        const cvFile = cvFileInput.files[0];
        const jobDesc = jobDescriptionInput.value.trim();

        if (!isDemo && !cvFile && !jobDesc) {
            showError("Please upload a CV or paste a job description.");
            return;
        }

        // Reset UI
        hideError();
        resultsSection.style.display = 'none';
        emptyState.style.display = 'none';
        loader.style.display = 'block';

        try {
            if (isDemo) {
                // Simulate delay
                await new Promise(resolve => setTimeout(resolve, 1500));
                renderResults(getDemoData());
            } else {
                const formData = new FormData();
                if (cvFile) formData.append('file', cvFile);
                formData.append('job_description', jobDesc);

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Server returned ${response.status}: ${errorText.substring(0, 100)}`);
                }

                const data = await response.json();
                renderResults(data);
            }
        } catch (err) {
            showError(`Analysis failed: ${err.message}`);
            emptyState.style.display = 'block';
        } finally {
            loader.style.display = 'none';
        }
    });

    clearResultsBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        emptyState.style.display = 'block';
        clearResultsBtn.style.display = 'none';
        analysisResult = null;
    });

    // --- Rendering Helpers ---
    function renderResults(data) {
        analysisResult = data;
        resultsSection.style.display = 'block';
        clearResultsBtn.style.display = 'block';

        // Overview
        document.getElementById('matchScoreVal').textContent = `${Math.round(data.match_score)}%`;
        document.getElementById('matchScoreFill').style.width = `${data.match_score}%`;
        
        document.getElementById('atsScoreVal').textContent = `${Math.round(data.ats_score)}%`;
        document.getElementById('atsScoreFill').style.width = `${data.ats_score}%`;
        
        document.getElementById('matchedSkillsCount').textContent = data.matched_skills.length;
        document.getElementById('missingSkillsCount').textContent = data.missing_skills.length;

        // Skills Tags
        renderTags('matchedSkillsTags', data.matched_skills, 'tag-good');
        renderTags('missingSkillsTags', data.missing_skills, 'tag-bad');

        // All Skills Lists
        renderList('cvSkillsList', data.cv_skills);
        renderList('jobSkillsList', data.job_skills);

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
                    <p>Builds: <strong>${course.skill}</strong></p>
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

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.style.display = 'block';
    }

    function hideError() {
        errorMsg.style.display = 'none';
        errorMsg.textContent = '';
    }
});
