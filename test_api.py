#!/usr/bin/env python3
"""
Test script for the Python Quiz API.
This script demonstrates how to interact with the API using the requests library.

Make sure the API server is running before executing this script:
    python main.py

Then run this script:
    python test_api.py
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_separator():
    """Print a separator line for better readability."""
    print("\n" + "-" * 50 + "\n")

def test_root_endpoint():
    """Test the root endpoint."""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    print_separator()
    return response.status_code == 200

def test_get_all_questions():
    """Test getting all questions."""
    print("Testing get all questions endpoint...")
    response = requests.get(f"{BASE_URL}/questions")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Number of questions: {len(data)}")
    print(f"First question: {json.dumps(data[0], indent=2)}")
    
    print_separator()
    return response.status_code == 200

def test_get_random_question():
    """Test getting a random question."""
    print("Testing get random question endpoint...")
    response = requests.get(f"{BASE_URL}/questions/random")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Random question: {json.dumps(data, indent=2)}")
    
    print_separator()
    return response.status_code == 200

def test_get_question_by_id():
    """Test getting a question by ID."""
    question_id = 1
    print(f"Testing get question by ID endpoint (ID: {question_id})...")
    response = requests.get(f"{BASE_URL}/questions/{question_id}")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Question: {json.dumps(data, indent=2)}")
    
    print_separator()
    return response.status_code == 200

def test_submit_answer():
    """Test submitting an answer."""
    # First get a random question
    response = requests.get(f"{BASE_URL}/questions/random")
    question = response.json()
    question_id = question["id"]
    correct_answer = question["correct_answer"]
    
    print(f"Testing submit answer endpoint...")
    print(f"Question: {question['question']}")
    print(f"Correct answer: {correct_answer}")
    
    # Submit the correct answer
    response = requests.post(
        f"{BASE_URL}/answer",
        json={"question_id": question_id, "answer": correct_answer}
    )
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    print_separator()
    return response.status_code == 200 and data["correct"] == True

def test_stats():
    """Test getting statistics."""
    print("Testing get stats endpoint...")
    response = requests.get(f"{BASE_URL}/stats")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Stats: {json.dumps(data, indent=2)}")
    
    print_separator()
    return response.status_code == 200

def test_reset_stats():
    """Test resetting statistics."""
    print("Testing reset stats endpoint...")
    response = requests.post(f"{BASE_URL}/reset")
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    # Verify stats were reset
    stats_response = requests.get(f"{BASE_URL}/stats")
    stats_data = stats_response.json()
    print(f"Stats after reset: {json.dumps(stats_data, indent=2)}")
    
    print_separator()
    return response.status_code == 200 and stats_data["questions_answered"] == 0

def run_all_tests():
    """Run all tests and report results."""
    print("Starting API tests...\n")
    
    # Wait for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Get All Questions", test_get_all_questions),
        ("Get Random Question", test_get_random_question),
        ("Get Question by ID", test_get_question_by_id),
        ("Submit Answer", test_submit_answer),
        ("Get Stats", test_stats),
        ("Reset Stats", test_reset_stats)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error in {name} test: {str(e)}")
            results.append((name, False))
    
    # Print summary
    print("\nTest Results Summary:")
    print("-" * 50)
    all_passed = True
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        if not result:
            all_passed = False
        print(f"{name}: {status}")
    
    print("-" * 50)
    if all_passed:
        print("\nAll tests passed! The API is working correctly.")
    else:
        print("\nSome tests failed. Please check the API implementation.")

if __name__ == "__main__":
    run_all_tests()