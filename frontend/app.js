const resumeInput = document.getElementById("resume");
const jdInput = document.getElementById("jobDescription");

const resumeFileName = document.getElementById("resumeFileName");
const jdFileName = document.getElementById("jdFileName");

const analyzeButton = document.getElementById("analyzeButton");
const statusElement = document.getElementById("status");
const loadingElement = document.getElementById("loading");

const matchResult = document.getElementById("matchResult");
const skillGapResult = document.getElementById("skillGapResult");
const resumeResult = document.getElementById("resumeResult");
const coverLetterResult = document.getElementById("coverLetterResult");
const interviewResult = document.getElementById("interviewResult");
const criticResult = document.getElementById("criticResult");

const downloadResume = document.getElementById("downloadResume");
const downloadCoverLetter = document.getElementById("downloadCoverLetter");


// ======================================================
// FILE NAME DISPLAY
// ======================================================

resumeInput.addEventListener("change", function () {
    if (resumeInput.files.length > 0) {
        resumeFileName.textContent = resumeInput.files[0].name;
    } else {
        resumeFileName.textContent = "No file selected";
    }
});


jdInput.addEventListener("change", function () {
    if (jdInput.files.length > 0) {
        jdFileName.textContent = jdInput.files[0].name;
    } else {
        jdFileName.textContent = "No file selected";
    }
});


// ======================================================
// HTML ESCAPE
// ======================================================

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ======================================================
// GENERIC RENDER
// ======================================================

function renderValue(value) {

    if (value === null || value === undefined) {
        return `<p class="empty-result">No result available.</p>`;
    }

    if (typeof value === "string") {
        return `
            <div class="result-content">
                <pre>${escapeHtml(value)}</pre>
            </div>
        `;
    }

    return `
        <div class="result-content">
            <pre>${escapeHtml(
                JSON.stringify(value, null, 2)
            )}</pre>
        </div>
    `;
}


// ======================================================
// TAGS
// ======================================================

function renderTags(items, type = "") {

    if (!Array.isArray(items) || items.length === 0) {
        return `<span class="empty-result">None</span>`;
    }

    return `
        <div class="tags">
            ${items.map(function (item) {
                return `
                    <span class="tag ${type}">
                        ${escapeHtml(item)}
                    </span>
                `;
            }).join("")}
        </div>
    `;
}


// ======================================================
// MATCH RESULT
// ======================================================

function renderMatchResult(data) {

    if (!data || typeof data !== "object") {
        matchResult.innerHTML = renderValue(data);
        return;
    }

    const score =
        data.match_score ??
        data.score ??
        data.match_percentage;

    if (score === undefined) {
        matchResult.innerHTML = renderValue(data);
        return;
    }

    const numericScore = Math.max(
        0,
        Math.min(100, Number(score))
    );

    let html = `
        <div class="score-container">

            <div class="score-circle">
                <span>${numericScore}%</span>
            </div>

            <div class="score-details">
                <h4>Resume Match Score</h4>

                <p>
                    Based on the skills and requirements
                    identified from the job description.
                </p>
            </div>

        </div>
    `;

    if (Array.isArray(data.matched_skills)) {

        html += `
            <br>

            <strong>Matched Skills</strong>

            ${renderTags(
                data.matched_skills,
                "success"
            )}
        `;
    }

    if (Array.isArray(data.missing_skills)) {

        html += `
            <br>

            <strong>Missing Skills</strong>

            ${renderTags(
                data.missing_skills,
                "missing"
            )}
        `;
    }

    matchResult.innerHTML = html;
}


// ======================================================
// SKILL GAP
// ======================================================

function renderSkillGap(data) {

    if (!data || typeof data !== "object") {
        skillGapResult.innerHTML = renderValue(data);
        return;
    }

    const missing =
        data.missing_skills ||
        data.skill_gaps ||
        [];

    const strengths =
        data.strengths ||
        data.matched_skills ||
        [];

    skillGapResult.innerHTML = `
        <div>

            <strong>💪 Strengths</strong>

            ${renderTags(
                strengths,
                "success"
            )}

        </div>

        <br>

        <div>

            <strong>⚠️ Skills to Improve</strong>

            ${renderTags(
                missing,
                "missing"
            )}

        </div>
    `;
}


// ======================================================
// TAILORED RESUME
// ======================================================

function renderResume(data) {

    if (!data) {
        resumeResult.innerHTML = renderValue(data);
        return;
    }

    if (typeof data === "string") {
        resumeResult.innerHTML = renderValue(data);
        return;
    }

    let html = "";

    if (data.summary) {

        html += `
            <h4>Professional Summary</h4>

            <p>
                ${escapeHtml(data.summary)}
            </p>

            <br>
        `;
    }

    if (Array.isArray(data.skills)) {

        html += `
            <h4>Skills</h4>

            ${renderTags(data.skills)}

            <br>
        `;
    }

    if (Array.isArray(data.experience)) {

        html += `
            <h4>Experience</h4>
        `;

        data.experience.forEach(function (item) {

            html += `
                <p>
                    <strong>
                        ${escapeHtml(
                            item.title ||
                            item.role ||
                            "Experience"
                        )}
                    </strong>
                </p>

                <p>
                    ${escapeHtml(
                        item.description ||
                        item.bullets ||
                        ""
                    )}
                </p>

                <br>
            `;
        });
    }

    if (html) {

        resumeResult.innerHTML = `
            <div class="result-content">
                ${html}
            </div>
        `;

    } else {

        resumeResult.innerHTML = renderValue(data);
    }
}


// ======================================================
// COVER LETTER
// ======================================================

function renderCoverLetter(data) {

    if (!data) {
        coverLetterResult.innerHTML = renderValue(data);
        return;
    }

    if (typeof data === "string") {

        coverLetterResult.innerHTML = `
            <div class="result-content">
                <pre>${escapeHtml(data)}</pre>
            </div>
        `;

        return;
    }

    if (data.full_cover_letter) {

        coverLetterResult.innerHTML = `
            <div class="result-content">
                <pre>${escapeHtml(
                    data.full_cover_letter
                )}</pre>
            </div>
        `;

        return;
    }

    coverLetterResult.innerHTML = renderValue(data);
}


// ======================================================
// INTERVIEW
// ======================================================

function renderInterview(data) {

    if (!data) {
        interviewResult.innerHTML = renderValue(data);
        return;
    }

    if (typeof data === "string") {
        interviewResult.innerHTML = renderValue(data);
        return;
    }

    let html = "";

    const questions =
        data.questions ||
        data.technical_questions ||
        [];

    if (
        Array.isArray(questions) &&
        questions.length > 0
    ) {

        html += `
            <h4>🎯 Interview Questions</h4>

            <ul class="result-list">
        `;

        questions.forEach(function (question) {

            if (typeof question === "string") {

                html += `
                    <li>
                        ${escapeHtml(question)}
                    </li>
                `;

            } else {

                html += `
                    <li>
                        ${escapeHtml(
                            question.question ||
                            question.text ||
                            JSON.stringify(question)
                        )}
                    </li>
                `;
            }
        });

        html += `
            </ul>
        `;
    }

    if (data.preparation_tips) {

        let tips = data.preparation_tips;

        if (Array.isArray(tips)) {
            tips = tips.join(" • ");
        }

        html += `
            <br>

            <h4>💡 Preparation Tips</h4>

            <p>
                ${escapeHtml(tips)}
            </p>
        `;
    }

    interviewResult.innerHTML =
        html || renderValue(data);
}


// ======================================================
// CRITIC
// ======================================================

function renderCritic(data) {

    if (!data || typeof data !== "object") {
        criticResult.innerHTML = renderValue(data);
        return;
    }

    const score =
        data.overall_score ??
        data.score;

    let html = "";

    if (score !== undefined) {

        html += `
            <div class="score-container">

                <div class="score-circle">
                    <span>${escapeHtml(score)}</span>
                </div>

                <div class="score-details">

                    <h4>
                        ${
                            data.passed
                                ? "✅ Passed"
                                : "⚠️ Needs Improvement"
                        }
                    </h4>

                    <p>
                        AI evaluation of the tailored resume.
                    </p>

                </div>

            </div>

            <br>
        `;
    }

    if (Array.isArray(data.strengths)) {

        html += `
            <strong>💪 Strengths</strong>

            <ul class="result-list">

                ${data.strengths.map(function (item) {
                    return `
                        <li>
                            ${escapeHtml(item)}
                        </li>
                    `;
                }).join("")}

            </ul>

            <br>
        `;
    }

    if (Array.isArray(data.issues)) {

        html += `
            <strong>⚠️ Issues</strong>

            <ul class="result-list">

                ${data.issues.map(function (item) {
                    return `
                        <li>
                            ${escapeHtml(item)}
                        </li>
                    `;
                }).join("")}

            </ul>
        `;
    }

    if (data.summary) {

        html += `
            <br>

            <strong>Summary</strong>

            <p>
                ${escapeHtml(data.summary)}
            </p>
        `;
    }

    criticResult.innerHTML =
        html || renderValue(data);
}


// ======================================================
// DISPLAY RESULTS
// ======================================================

function displayResults(result) {

    if (!result) {
        return;
    }

    renderMatchResult(
        result.matching_result
    );

    renderSkillGap(
        result.skill_gap_analysis
    );

    renderResume(
        result.tailored_resume
    );

    renderCoverLetter(
        result.cover_letter
    );

    renderInterview(
        result.interview_preparation
    );

    renderCritic(
        result.critic_result
    );
}


// ======================================================
// ANALYZE RESUME
// ======================================================

async function analyzeResume() {

    const resume = resumeInput.files[0];
    const jobDescription = jdInput.files[0];

    if (!resume || !jobDescription) {

        statusElement.textContent =
            "Please upload both Resume and Job Description.";

        statusElement.className =
            "status error";

        return;
    }

    const allowedExtensions = [
        ".pdf",
        ".docx"
    ];

    const resumeExtension =
        resume.name
            .substring(
                resume.name.lastIndexOf(".")
            )
            .toLowerCase();

    const jdExtension =
        jobDescription.name
            .substring(
                jobDescription.name.lastIndexOf(".")
            )
            .toLowerCase();

    if (
        !allowedExtensions.includes(resumeExtension) ||
        !allowedExtensions.includes(jdExtension)
    ) {

        statusElement.textContent =
            "Only PDF and DOCX files are supported.";

        statusElement.className =
            "status error";

        return;
    }

    const formData = new FormData();

    formData.append(
        "resume",
        resume
    );

    formData.append(
        "job_description",
        jobDescription
    );

    analyzeButton.disabled = true;

    loadingElement.classList.add("active");

    statusElement.textContent =
        "AI agents are analyzing your documents...";

    statusElement.className =
        "status";

    try {

        const response = await fetch(
            "/workflow/?max_revisions=2",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Workflow request failed."
            );
        }

        displayResults(data.result);

        statusElement.textContent =
            "✅ Analysis completed successfully.";

        statusElement.className =
            "status success";

    } catch (error) {

        console.error(error);

        statusElement.textContent =
            `❌ ${error.message}`;

        statusElement.className =
            "status error";

    } finally {

        analyzeButton.disabled = false;

        loadingElement.classList.remove("active");
    }
}


// ======================================================
// ANALYZE BUTTON
// ======================================================

analyzeButton.addEventListener(
    "click",
    analyzeResume
);


// ======================================================
// DOWNLOAD TEXT FILE
// ======================================================

function downloadTextFile(
    filename,
    content
) {

    const blob = new Blob(
        [content],
        {
            type: "text/plain;charset=utf-8"
        }
    );

    const url =
        URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    link.href = url;

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}


// ======================================================
// DOWNLOAD RESUME
// ======================================================

downloadResume.addEventListener(
    "click",
    function () {

        const content =
            resumeResult.innerText.trim();

        if (!content) {

            alert(
                "No tailored resume available."
            );

            return;
        }

        downloadTextFile(
            "tailored_resume.txt",
            content
        );
    }
);


// ======================================================
// DOWNLOAD COVER LETTER
// ======================================================

downloadCoverLetter.addEventListener(
    "click",
    function () {

        const content =
            coverLetterResult.innerText.trim();

        if (!content) {

            alert(
                "No cover letter available."
            );

            return;
        }

        downloadTextFile(
            "cover_letter.txt",
            content
        );
    }
);
// ======================================================
// MOCK DASHBOARD TEST
// ======================================================

const mockButton = document.getElementById("mockButton");

const mockData = {
    matching_result: {
        match_score: 78,
        matched_skills: [
            "Java",
            "Python",
            "SQL",
            "Data Structures",
            "Git"
        ],
        missing_skills: [
            "Spring Boot",
            "Docker",
            "AWS"
        ]
    },

    skill_gap_analysis: {
        strengths: [
            "Java",
            "Python",
            "SQL",
            "Data Structures",
            "Git"
        ],
        missing_skills: [
            "Spring Boot",
            "Docker",
            "AWS"
        ]
    },

    tailored_resume: {
        summary:
            "Computer Science student with strong programming fundamentals in Java and Python, experienced in SQL, data structures and backend development. Interested in building scalable software solutions.",

        skills: [
            "Java",
            "Python",
            "SQL",
            "Data Structures",
            "Git",
            "REST APIs"
        ],

        experience: [
            {
                title: "Software Development Project",

                description:
                    "Developed a backend application using Python and REST APIs. Implemented database operations using SQL and designed efficient data structures for application functionality."
            }
        ]
    },

    cover_letter: {
        full_cover_letter:
`Dear Hiring Manager,

I am excited to apply for the Software Development position at your organization.

My background in Java, Python, SQL, data structures and backend development has given me a strong foundation for building reliable software applications.

I am particularly interested in this opportunity because it would allow me to apply my technical skills while continuing to learn modern software development practices.

Thank you for considering my application.

Sincerely,
Candidate`
    },

    interview_preparation: {
        questions: [
            "Explain the difference between ArrayList and LinkedList in Java.",
            "What are the four pillars of Object-Oriented Programming?",
            "How does a HashMap work internally?",
            "Explain the difference between SQL JOIN types.",
            "How would you design a REST API?",
            "What is the difference between authentication and authorization?",
            "Explain one project you have worked on and your contribution."
        ],

        preparation_tips: [
            "Revise Java OOP concepts",
            "Practice SQL queries",
            "Review data structures",
            "Prepare your project explanation",
            "Practice behavioral questions"
        ]
    },

    critic_result: {
        overall_score: 86,
        passed: true,

        strengths: [
            "Good keyword alignment",
            "Skills are relevant to the job",
            "Resume content is concise",
            "No obvious unsupported claims"
        ],

        issues: [
            "Could add more measurable project results",
            "Spring Boot experience is missing"
        ],

        summary:
            "The tailored resume has strong alignment with the target job and is suitable for further refinement."
    }
};


// ======================================================
// MOCK BUTTON ACTION
// ======================================================

mockButton.addEventListener("click", function () {

    statusElement.textContent =
        "🧪 Loading demo dashboard...";

    statusElement.className =
        "status";

    loadingElement.classList.add("active");

    setTimeout(function () {

        displayResults(mockData);

        loadingElement.classList.remove("active");

        statusElement.textContent =
            "✅ Demo dashboard loaded successfully.";

        statusElement.className =
            "status success";

        document.getElementById("results")
            .scrollIntoView({
                behavior: "smooth"
            });

    }, 800);
});