// API Base URL - change this to match your server
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const welcomeScreen = document.getElementById('welcome-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultsScreen = document.getElementById('results-screen');
const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const feedbackContainer = document.getElementById('feedback-container');
const feedbackText = document.getElementById('feedback-text');
const questionsAnswered = document.getElementById('questions-answered');
const correctAnswers = document.getElementById('correct-answers');
const accuracyElement = document.getElementById('accuracy');

// Buttons
const startQuizBtn = document.getElementById('start-quiz-btn');
const nextQuestionBtn = document.getElementById('next-question-btn');
const restartQuizBtn = document.getElementById('restart-quiz-btn');

// Quiz state
let currentQuestion = null;
let selectedOption = null;

// Event Listeners
startQuizBtn.addEventListener('click', startQuiz);
nextQuestionBtn.addEventListener('click', getNextQuestion);
restartQuizBtn.addEventListener('click', restartQuiz);

/**
 * Initialize the application
 */
function init() {
    // Reset the quiz state on the server
    resetQuizState()
        .then(() => {
            console.log('Quiz state reset successfully');
        })
        .catch(error => {
            console.error('Error resetting quiz state:', error);
        });
}

/**
 * Start the quiz
 */
function startQuiz() {
    welcomeScreen.classList.add('hidden');
    quizScreen.classList.remove('hidden');
    getNextQuestion();
}

/**
 * Get a random question from the API
 */
function getNextQuestion() {
    // Hide feedback container
    feedbackContainer.classList.add('hidden');
    
    // Fetch a random question
    fetch(`${API_BASE_URL}/questions/random`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(question => {
            displayQuestion(question);
        })
        .catch(error => {
            console.error('Error fetching question:', error);
            alert('Failed to load question. Please try again.');
        });
}

/**
 * Display a question on the screen
 */
function displayQuestion(question) {
    currentQuestion = question;
    
    // Set question text
    questionText.textContent = question.question;
    
    // Clear previous options
    optionsContainer.innerHTML = '';
    
    // Add options
    question.options.forEach(option => {
        const optionButton = document.createElement('button');
        optionButton.classList.add('option-btn');
        optionButton.dataset.id = option.id;
        optionButton.textContent = `${option.id}) ${option.text}`;
        
        optionButton.addEventListener('click', () => selectOption(optionButton, option.id));
        
        optionsContainer.appendChild(optionButton);
    });
}

/**
 * Handle option selection
 */
function selectOption(optionElement, optionId) {
    // Clear previous selection
    const options = document.querySelectorAll('.option-btn');
    options.forEach(opt => opt.classList.remove('selected'));
    
    // Mark selected option
    optionElement.classList.add('selected');
    selectedOption = optionId;
    
    // Submit answer
    submitAnswer(currentQuestion.id, optionId);
}

/**
 * Submit an answer to the API
 */
function submitAnswer(questionId, answer) {
    fetch(`${API_BASE_URL}/answer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            answer: answer
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        showFeedback(data);
    })
    .catch(error => {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer. Please try again.');
    });
}

/**
 * Show feedback for the answer
 */
function showFeedback(data) {
    // Mark correct/incorrect options
    const options = document.querySelectorAll('.option-btn');
    options.forEach(opt => {
        const optionId = opt.dataset.id;
        
        if (optionId === data.correct_answer) {
            opt.classList.add('correct');
        } else if (optionId === selectedOption && !data.correct) {
            opt.classList.add('incorrect');
        }
        
        // Disable all options
        opt.disabled = true;
    });
    
    // Show feedback
    feedbackText.textContent = data.message;
    feedbackContainer.classList.remove('hidden');
    
    // Update stats
    updateStats();
}

/**
 * Update quiz statistics
 */
function updateStats() {
    fetch(`${API_BASE_URL}/stats`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(stats => {
            // If we've answered 5 questions, show results screen
            if (stats.questions_answered >= 5) {
                showResults(stats);
            }
        })
        .catch(error => {
            console.error('Error fetching stats:', error);
        });
}

/**
 * Show quiz results
 */
function showResults(stats) {
    quizScreen.classList.add('hidden');
    resultsScreen.classList.remove('hidden');
    
    questionsAnswered.textContent = stats.questions_answered;
    correctAnswers.textContent = stats.correct_answers;
    accuracyElement.textContent = `${Math.round(stats.accuracy * 100)}%`;
}

/**
 * Reset quiz state on the server
 */
function resetQuizState() {
    return fetch(`${API_BASE_URL}/reset`, {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}

/**
 * Restart the quiz
 */
function restartQuiz() {
    resetQuizState()
        .then(() => {
            resultsScreen.classList.add('hidden');
            welcomeScreen.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error resetting quiz:', error);
            alert('Failed to reset quiz. Please try again.');
        });
}

// Initialize the application
document.addEventListener('DOMContentLoaded', init);