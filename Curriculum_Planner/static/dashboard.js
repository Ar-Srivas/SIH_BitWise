// dashboard.js
let userEmail = '';

document.addEventListener('DOMContentLoaded', function() {
    // Get email from URL
    const urlParams = new URLSearchParams(window.location.search);
    userEmail = urlParams.get('email');

    if (!userEmail) {
        location.href = '/';
        return;
    }

    // Set time-based greeting
    const greeting = document.getElementById('greeting');
    const hour = new Date().getHours();
    if (hour < 12) {
        greeting.textContent = "Good morning!";
    } else if (hour < 18) {
        greeting.textContent = "Good afternoon!";
    } else {
        greeting.textContent = "Good evening!";
    }
    // Setup quiz button
    const quizButton = document.getElementById('take-quiz-btn');
    quizButton.onclick = function() {
        location.href = `/quiz?email=${userEmail}`;
    };
    // Load user profile and quiz results
    loadQuizResults();
});

function loadQuizResults() {
    fetch(`/api/profile?email=${userEmail}`)
    .then(response => response.json())
    .then(data => {
    const quizResults = document.getElementById('quiz-results');

    if (data.quiz_results && Object.keys(data.quiz_results).length > 0) {
        let resultsHtml = '<div class="results-grid">';

        for (const [category, count] of Object.entries(data.quiz_results)) {
            resultsHtml += `
                <div class="result-card">
                    <h3>${category}</h3>
                    <p class="result-count">${count}</p>
                </div>
            `;
        }

        resultsHtml += '</div>';
        quizResults.innerHTML = resultsHtml;
    } else {
        quizResults.innerHTML = `
            <p class="no-results">
                You haven't taken any quizzes yet.
                <a href="/quiz?email=${userEmail}" style="color: var(--primary-color);">Take a quiz</a>
                to see your results here.
            </p>
        `;
    }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('quiz-results').innerHTML =
            '<p class="error">Failed to load your results. Please try again later.</p>';
    });
}

// All navigation functions are now correct and non-duplicated

function goToProfile() {
    location.href = `/profile?email=${userEmail}`;
}

function signOut() {
    location.href = '/';
}

function goToRecommendations() {
    location.href = `/select_subject/${userEmail}`;
}

function goToSlotBooking() {
    location.href = `/slot_booking_students?email=${userEmail}`;
}

function goToChatBot(){
    location.href = `/chat?email=${userEmail}`;
}

function goToPrediction() {
    location.href = "/predict";
}