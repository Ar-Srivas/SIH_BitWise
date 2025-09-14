let quizData = [];
let currentQuestion = "q1";
let quizResult = {};
let userEmail = '';

const questionEl = document.getElementById('question');
const optionsEl = document.getElementById('options');

document.addEventListener('DOMContentLoaded', function() {
    // Get email from URL
    const urlParams = new URLSearchParams(window.location.search);
    userEmail = urlParams.get('email');

    if (!userEmail) {
        location.href = '/';
        return;
    }

    // Setup back button
    const backBtn = document.getElementById('back-to-dashboard');
    backBtn.onclick = function() {
        location.href = `/dashboard?email=${userEmail}`;
    };

    // Load quiz questions
    fetchQuestions();
});

async function fetchQuestions() {
    try {
        const response = await fetch('/static/questions.json');
        quizData = await response.json();
        loadQuestion(currentQuestion);
    } catch (error) {
        console.error('Error fetching questions:', error);
        questionEl.textContent = 'Failed to load questions. Please try again later.';
    }
}

function loadQuestion(questionId) {
    const currentQuiz = quizData.find(q => q.id === questionId);
    if (!currentQuiz) {
        endQuiz();
        return;
    }

    questionEl.textContent = currentQuiz.question;
    optionsEl.innerHTML = '';

    currentQuiz.options.forEach(option => {
        const button = document.createElement('button');
        button.classList.add('option');
        button.textContent = option.text;
        button.onclick = () => selectAnswer(option);
        optionsEl.appendChild(button);
    });
}

function selectAnswer(selectedOption) {
    // Record the answer if it has a category
    if (selectedOption.category) {
        if (!quizResult[selectedOption.category]) {
            quizResult[selectedOption.category] = 0;
        }
        quizResult[selectedOption.category]++;
    }

    // Move to next question or end quiz
    if (selectedOption.next) {
        currentQuestion = selectedOption.next;
        loadQuestion(currentQuestion);
    } else {
        endQuiz();
    }
}

function endQuiz() {
    questionEl.textContent = "Quiz completed! Here are your results:";
    optionsEl.innerHTML = '';

    // Display results
    if (Object.keys(quizResult).length > 0) {
        Object.entries(quizResult).forEach(([category, count]) => {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'result-item';
            resultDiv.innerHTML = `<strong>${category}:</strong> ${count}`;
            optionsEl.appendChild(resultDiv);
        });
    } else {
        const noResults = document.createElement('p');
        noResults.textContent = 'No results to display.';
        optionsEl.appendChild(noResults);
    }

    // Save results to the database
    saveQuizResults();
}

function saveQuizResults() {
    if (Object.keys(quizResult).length === 0) {
        return;
    }

    fetch('/submit-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `email=${userEmail}&quiz_result=${encodeURIComponent(JSON.stringify(quizResult))}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const successMsg = document.createElement('p');
            successMsg.textContent = 'Results saved successfully!';
            successMsg.style.color = 'green';
            successMsg.style.marginTop = '1rem';
            optionsEl.appendChild(successMsg);
        } else {
            throw new Error('Failed to save results');
        }
    })
    .catch(error => {
        console.error('Error saving results:', error);
        const errorMsg = document.createElement('p');
        errorMsg.textContent = 'Failed to save results, but you can still return to the dashboard.';
        errorMsg.style.color = 'red';
        errorMsg.style.marginTop = '1rem';
        optionsEl.appendChild(errorMsg);
    });
}