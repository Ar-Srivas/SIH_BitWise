// static/subject.js

function goToRecommendations() {
    const subject = document.getElementById('subjectSelect').value;
    const studentId = "DS07"; // Hardcoded student ID for this example
    if (subject) {
        // Construct the URL with both the studentId and the subject
        window.location.href = `/recommend/${studentId}/${subject}`;
    } else {
        alert("Please select a subject.");
    }
}