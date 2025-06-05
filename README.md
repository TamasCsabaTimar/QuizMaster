# Python Quiz API

A RESTful API for a Python quiz application built with FastAPI. This API provides endpoints for retrieving quiz questions, submitting answers, and tracking quiz statistics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Frontend Application](#frontend-application)
- [Example Usage](#example-usage)

## Features

- Retrieve all quiz questions or a specific question by ID
- Get a random question for quiz sessions
- Submit answers and receive immediate feedback
- Track quiz statistics (questions answered, correct answers, accuracy)
- Reset quiz progress
- Automatic API documentation with Swagger UI and ReDoc

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd QuizMaster
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the API

To start the API server:

```
python main.py
```

Or using uvicorn directly:

```
uvicorn main:app --reload
```

### Using Batch Files

For convenience, several batch files are provided to start and restart the application:

1. **start_app.bat** - Starts the application using Python directly:
   ```
   start_app.bat
   ```

2. **restart_app.bat** - Restarts the application by stopping any running instances and starting it again:
   ```
   restart_app.bat
   ```

3. **restart_uvicorn.bat** - Restarts the application using Uvicorn with hot-reload enabled:
   ```
   restart_uvicorn.bat
   ```

The API will be available at http://localhost:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Root endpoint with API information |
| GET | /questions | Get all available quiz questions |
| GET | /questions/{question_id} | Get a specific question by ID |
| GET | /questions/random | Get a random question |
| POST | /answer | Submit an answer to a question |
| GET | /stats | Get current quiz statistics |
| POST | /reset | Reset quiz statistics |

### API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Data Models

### Question

```json
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
}
```

### Answer Request

```json
{
  "question_id": 1,
  "answer": "b"
}
```

### Answer Response

```json
{
  "correct": true,
  "correct_answer": "b",
  "message": "Correct! Well done!"
}
```

### Statistics Response

```json
{
  "questions_answered": 5,
  "correct_answers": 3,
  "accuracy": 0.6
}
```

## Testing the API

A test script is included to verify that all API endpoints are working correctly. To run the tests:

1. Start the API server in one terminal:
   ```
   python main.py
   ```

2. Run the test script in another terminal:
   ```
   python test_api.py
   ```

The test script will:
- Test all API endpoints
- Display detailed information about each request and response
- Provide a summary of test results

This script also serves as an example of how to interact with the API using Python's requests library.

## Frontend Application

A complete frontend application for the Python Quiz API is included in the `/frontend` directory. This is a responsive web application built with HTML, CSS, and JavaScript that provides a user-friendly interface for taking the Python quiz.

### Frontend Features

- Clean, modern UI with responsive design
- Interactive quiz flow with immediate feedback
- Results screen with quiz statistics
- No external libraries or frameworks - pure HTML, CSS, and JavaScript

### Running the Frontend

1. Make sure the API server is running:
   ```
   python main.py
   ```

2. Open the `frontend/index.html` file in your web browser.
   - You can use a simple HTTP server like Python's built-in server:
     ```
     # Python 3
     python -m http.server

     # Then navigate to http://localhost:8000/frontend/
     ```

3. If the API is running on a different URL than `http://localhost:8000`, update the `API_BASE_URL` variable in `frontend/script.js`.

### Frontend Structure

- `frontend/index.html` - The main HTML structure
- `frontend/styles.css` - CSS styling for the application
- `frontend/script.js` - JavaScript functionality to interact with the API
- `frontend/README.md` - Detailed documentation for the frontend

### Screenshots

The frontend application includes:
- A welcome screen with instructions
- The quiz interface with multiple-choice questions
- Immediate feedback on answers
- A results screen showing quiz statistics

## Example Usage

### API Integration

Here's an example of how to integrate this API with a custom frontend application using JavaScript:

```javascript
// Get a random question
async function getRandomQuestion() {
  const response = await fetch('http://localhost:8000/questions/random');
  const question = await response.json();
  return question;
}

// Submit an answer
async function submitAnswer(questionId, answer) {
  const response = await fetch('http://localhost:8000/answer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question_id: questionId,
      answer: answer
    }),
  });
  const result = await response.json();
  return result;
}

// Get quiz statistics
async function getStats() {
  const response = await fetch('http://localhost:8000/stats');
  const stats = await response.json();
  return stats;
}
```

### Python Client

Here's an example of how to use the API with Python's requests library:

```python
import requests

# Get a random question
response = requests.get('http://localhost:8000/questions/random')
question = response.json()
print(f"Question: {question['question']}")
for option in question['options']:
    print(f"{option['id']}) {option['text']}")

# Submit an answer
answer = input("Your answer: ")
response = requests.post(
    'http://localhost:8000/answer',
    json={'question_id': question['id'], 'answer': answer}
)
result = response.json()
print(result['message'])

# Get statistics
response = requests.get('http://localhost:8000/stats')
stats = response.json()
print(f"Questions answered: {stats['questions_answered']}")
print(f"Correct answers: {stats['correct_answers']}")
print(f"Accuracy: {stats['accuracy']:.2%}")
```

## Troubleshooting

### Common Issues and Solutions

1. **Dependency Conflicts**:
   If you encounter errors related to incompatible dependencies, try using the exact versions specified in requirements.txt:
   ```
   pip install -r requirements.txt
   ```

   The current requirements.txt file specifies compatible versions of all dependencies.

2. **Port Already in Use**:
   If you see an error like "Address already in use", another process is using port 8000. You can:
   - Find and terminate the process using port 8000
   - Or modify the port in main.py (change the port number in the uvicorn.run() call)
   - Use the restart batch files which automatically handle terminating existing processes:
     ```
     restart_app.bat
     ```
     or
     ```
     restart_uvicorn.bat
     ```

3. **Virtual Environment Issues**:
   If you have problems with the virtual environment:
   - Make sure you've activated it correctly before installing dependencies
   - If activation fails, try recreating the virtual environment:
     ```
     python -m venv .venv --clear
     ```
   - Use the provided batch files which handle virtual environment activation automatically

4. **Import Errors**:
   If you see import errors when running the application, ensure all dependencies are installed:
   ```
   pip list
   ```
   Verify that fastapi, pydantic, uvicorn, and requests are listed with the correct versions.

5. **Application Needs Restarting**:
   If the application becomes unresponsive or you need to restart it after making changes:
   - Use the restart batch files to automatically stop and restart the application:
     ```
     restart_app.bat
     ```
     or for hot-reloading with uvicorn:
     ```
     restart_uvicorn.bat
     ```

## Future Enhancements

- User authentication and personalized quiz sessions
- Categorization of questions by difficulty or topic
- Timed quiz mode
- Persistent storage with a database
- More comprehensive statistics and analytics
