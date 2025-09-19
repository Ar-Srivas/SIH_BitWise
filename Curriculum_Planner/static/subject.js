function goToRecommendations() {
    const subject = document.getElementById('subjectSelect').value;
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email') || "s1"; // fallback to s1

    if (subject) {
        window.location.href = `/recommend/${email}/${subject}`;
    } else {
        alert("Please select a subject.");
    }
}