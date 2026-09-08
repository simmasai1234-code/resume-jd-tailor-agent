const resumeInput = document.getElementById("resume");
const jobDescriptionInput = document.getElementById("jobDescription");
const analyzeButton = document.getElementById("analyzeButton");
const statusElement = document.getElementById("status");

const resultsSection = document.getElementById("results");

const matchResult = document.getElementById("matchResult");
const skillGapResult = document.getElementById("skillGapResult");
const resumeResult = document.getElementById("resumeResult");
const coverLetterResult = document.getElementById("coverLetterResult");
const interviewResult = document.getElementById("interviewResult");
const criticResult = document.getElementById("criticResult");


/*
 * Convert JavaScript values into readable HTML.
 */
function renderValue(value) {

    if (value === null || value === undefined) {
        return "No data available";
    }

    if (typeof value === "object") {

        const formatted = JSON.stringify(value, null, 2);

        return `<pre>${escapeHtml(formatted)}</pre>`;
    }

    return `<pre>${escapeHtml(String(value))}</pre>`;
}


/*
 * Prevent JSON/text from being interpreted as HTML.
 */
function escapeHtml(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/*
 * Display workflow results.
 */
function displayResults(result) {

    const data = result.result || result;

    matchResult.innerHTML = renderValue(data.matching_result);

    skillGapResult.innerHTML =
        renderValue(data.skill_gap_analysis);

    resumeResult.innerHTML =
        renderValue(data.tailored_resume);

    coverLetterResult.innerHTML =
        renderValue(data.cover_letter);

    interviewResult.innerHTML =
        renderValue(data.interview_preparation);

    criticResult.innerHTML =
        renderValue(data.critic_result);

    resultsSection.style.display = "block";
}


/*
 * Analyze Resume + Job Description.
 */
analyzeButton.addEventListener("click", async () => {

    const resumeFile = resumeInput.files[0];
    const jobDescriptionFile = jobDescriptionInput.files[0];

    if (!resumeFile) {

        statusElement.textContent =
            "❌ Please select a Resume file.";

        return;
    }

    if (!jobDescriptionFile) {

        statusElement.textContent =
            "❌ Please select a Job Description file.";

        return;
    }


    const allowedExtensions = [".pdf", ".docx"];

    const resumeExtension =
        "." + resumeFile.name.split(".").pop().toLowerCase();

    const jdExtension =
        "." + jobDescriptionFile.name.split(".").pop().toLowerCase();


    if (!allowedExtensions.includes(resumeExtension)) {

        statusElement.textContent =
            "❌ Resume must be PDF or DOCX.";

        return;
    }

    if (!allowedExtensions.includes(jdExtension)) {

        statusElement.textContent =
            "❌ Job Description must be PDF or DOCX.";

        return;
    }


    /*
     * Prepare files for FastAPI.
     */
    const formData = new FormData();

    formData.append("resume", resumeFile);

    formData.append(
        "job_description",
        jobDescriptionFile
    );


    /*
     * Disable button while processing.
     */
    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "⏳ Analyzing...";

    statusElement.textContent =
        "🤖 AI agents are analyzing your resume...";


    try {

        /*
         * Call FastAPI end-to-end workflow.
         *
         * IMPORTANT:
         * We are not testing this endpoint yet because
         * Gemini API quota was previously exhausted.
         */
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
                "Workflow failed."
            );
        }


        displayResults(data);


        statusElement.textContent =
            "✅ Analysis completed successfully.";

    }
    catch (error) {

        console.error(error);

        statusElement.textContent =
            "❌ " + error.message;

    }
    finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "🚀 Analyze Resume";
    }

});