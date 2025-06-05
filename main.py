from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles



# Create FastAPI app
app = FastAPI(
    title="Python Quiz API",
    description="A REST API for a Python quiz application",
    version="1.0.0"
)
# A frontend fájlok kiszolgálása
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class Option(BaseModel):
    id: str  # a, b, c, or d
    text: str

class Question(BaseModel):
    id: int
    question: str
    options: List[Option]
    correct_answer: str

class AnswerRequest(BaseModel):
    question_id: int
    answer: str

class AnswerResponse(BaseModel):
    correct: bool
    correct_answer: str
    message: str

class QuizState(BaseModel):
    questions_answered: int = 0
    correct_answers: int = 0

# Initialize quiz questions from the original bot
questions = [
    {
        "id": 1,
        "question": "What is the correct way to create a variable named 'age' with the value 25?",
        "options": [
            {"id": "a", "text": "variable age = 25"},
            {"id": "b", "text": "age = 25"},
            {"id": "c", "text": "int age = 25"},
            {"id": "d", "text": "age := 25"}
        ],
        "correct_answer": "b"
    },
    {
        "id": 2,
        "question": "Which of the following is used to add a comment in Python?",
        "options": [
            {"id": "a", "text": "//"},
            {"id": "b", "text": "/* */"},
            {"id": "c", "text": "#"},
            {"id": "d", "text": "<!-- -->"}
        ],
        "correct_answer": "c"
    },
    {
        "id": 3,
        "question": "What does the 'len()' function do in Python?",
        "options": [
            {"id": "a", "text": "Returns the largest item in an iterable"},
            {"id": "b", "text": "Returns the length of an object"},
            {"id": "c", "text": "Returns the lowest item in an iterable"},
            {"id": "d", "text": "Returns the sum of all items in an iterable"}
        ],
        "correct_answer": "b"
    },
    {
        "id": 4,
        "question": "Which of the following is the correct way to create a list in Python?",
        "options": [
            {"id": "a", "text": "list = [1, 2, 3]"},
            {"id": "b", "text": "list = (1, 2, 3)"},
            {"id": "c", "text": "list = {1, 2, 3}"},
            {"id": "d", "text": "list = 1, 2, 3"}
        ],
        "correct_answer": "a"
    },
    {
        "id": 5,
        "question": "What is the output of print(2 ** 3)?",
        "options": [
            {"id": "a", "text": "6"},
            {"id": "b", "text": "5"},
            {"id": "c", "text": "8"},
            {"id": "d", "text": "Error"}
        ],
        "correct_answer": "c"
    }
]

# Store user quiz states (in a real application, this would be in a database)
user_states = {}

# API endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the Python Quiz API",
        "version": "1.0.0",
        "endpoints": {
            "GET /questions": "Get all questions",
            "GET /questions/random": "Get a random question",
            "POST /answer": "Submit an answer",
            "GET /stats": "Get quiz statistics",
            "POST /reset": "Reset quiz state"
        }
    }

@app.get("/questions", response_model=List[Question])
async def get_all_questions():
    """Get all available quiz questions"""
    return questions

@app.get("/questions/random", response_model=Question)
async def get_random_question():
    """Get a random question from the question bank"""
    return random.choice(questions)

@app.get("/questions/{question_id}", response_model=Question)
async def get_question(question_id: int):
    """Get a specific question by ID"""
    for question in questions:
        if question["id"] == question_id:
            return question
    raise HTTPException(status_code=404, detail="Question not found")

@app.post("/answer", response_model=AnswerResponse)
async def submit_answer(answer_request: AnswerRequest):
    """Submit an answer to a question and get feedback"""
    # Find the question
    question = None
    for q in questions:
        if q["id"] == answer_request.question_id:
            question = q
            break

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if the answer is correct
    is_correct = answer_request.answer.lower() == question["correct_answer"].lower()

    # Update user statistics (in a real app, this would be tied to user authentication)
    # For simplicity, we'll use a default user ID
    user_id = "default_user"
    if user_id not in user_states:
        user_states[user_id] = QuizState()

    user_states[user_id].questions_answered += 1
    if is_correct:
        user_states[user_id].correct_answers += 1

    # Prepare response
    if is_correct:
        message = "Correct! Well done!"
    else:
        message = f"Sorry, that's incorrect. The correct answer is {question['correct_answer']}."

    return {
        "correct": is_correct,
        "correct_answer": question["correct_answer"],
        "message": message
    }

@app.get("/stats")
async def get_stats():
    """Get current quiz statistics"""
    # For simplicity, we'll use a default user ID
    user_id = "default_user"
    if user_id not in user_states:
        user_states[user_id] = QuizState()

    state = user_states[user_id]
    return {
        "questions_answered": state.questions_answered,
        "correct_answers": state.correct_answers,
        "accuracy": state.correct_answers / state.questions_answered if state.questions_answered > 0 else 0
    }

@app.post("/reset")
async def reset_stats():
    """Reset quiz statistics"""
    # For simplicity, we'll use a default user ID
    user_id = "default_user"
    user_states[user_id] = QuizState()
    return {"message": "Quiz statistics have been reset"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
