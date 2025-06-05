# Python Quiz Master Frontend

This is the frontend for the Python Quiz Master application. It's a simple, responsive web application that interacts with the Python Quiz API to provide a user-friendly quiz experience.

## Features

- Clean, modern UI
- Responsive design that works on desktop and mobile
- Interactive quiz with immediate feedback
- Results screen with statistics
- Ability to restart the quiz

## Setup and Usage

1. Make sure the backend API server is running:
   ```
   python main.py
   ```

2. Open the `index.html` file in your web browser.
   - You can use a simple HTTP server like Python's built-in server:
     ```
     # Python 3
     python -m http.server
     
     # Then navigate to http://localhost:8000/frontend/
     ```

3. If the API is running on a different URL than `http://localhost:8000`, update the `API_BASE_URL` variable in `script.js`.

## Files

- `index.html` - The main HTML structure
- `styles.css` - CSS styling for the application
- `script.js` - JavaScript functionality to interact with the API

## Browser Compatibility

This application uses modern JavaScript and CSS features and should work in all modern browsers (Chrome, Firefox, Safari, Edge).

## CORS Configuration

If you encounter CORS (Cross-Origin Resource Sharing) issues, you may need to configure your API server to allow requests from the frontend's origin. For the FastAPI backend, you can add CORS middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## License

This project is open source and available under the MIT License.