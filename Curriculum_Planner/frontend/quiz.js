let quizData = [];
let currentQuestion = 0;
let score = 0;

const questionEl = document.querySelector('.question');
const optionsEl = document.querySelector('.options');
const nextBtn = document.querySelector('.next-btn');

async function fetchQuestions() {
    try {
        const response = await fetch('/frontend/questions.json');
        quizData = await response.json();
        loadQuestion();
    } catch (error) {
        console.error('Error fetching questions:', error);
        questionEl.textContent = 'Failed to load questions. Please try again later.';
    }
}

function loadQuestion() {
    const currentQuiz = quizData[currentQuestion];
    questionEl.textContent = currentQuiz.question;
    optionsEl.innerHTML = '';
    currentQuiz.options.forEach(option => {
        const button = document.createElement('button');
        button.classList.add('option');
        button.textContent = option;
        button.onclick = () => checkAnswer(option);
        optionsEl.appendChild(button);
    });
}

function checkAnswer(selectedOption) {
    const currentQuiz = quizData[currentQuestion];
    if (selectedOption === currentQuiz.answer) {
        score++;
    }
    nextBtn.disabled = false;
}

nextBtn.addEventListener('click', () => {
    currentQuestion++;
    if (currentQuestion < quizData.length) {
        loadQuestion();
        nextBtn.disabled = true;
    } else {
        endQuiz();
    }
});

function endQuiz() {
    questionEl.textContent = `Quiz completed! Your score is ${score}/${quizData.length}.`;
    optionsEl.innerHTML = '';
    nextBtn.style.display = 'none';
}

fetchQuestions();
nextBtn.disabled = true;