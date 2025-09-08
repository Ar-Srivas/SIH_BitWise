function viewProgress() {
    alert("Progress tracking feature coming soon!");
}

function viewProfile() {
    alert("Profile management feature coming soon!");
}

// Add some interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Add greeting based on time of day
    const header = document.querySelector('.title');
    const currentHour = new Date().getHours();
    let greeting;

    if (currentHour < 12) {
        greeting = "Good morning! Ready to learn today?";
    } else if (currentHour < 17) {
        greeting = "Good afternoon! Let's continue learning!";
    } else {
        greeting = "Good evening! Time for some learning!";
    }

    header.textContent = greeting;
});