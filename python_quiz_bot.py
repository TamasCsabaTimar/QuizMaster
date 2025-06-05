#!/usr/bin/env python3

import random

class PythonQuizBot:
    def __init__(self):
        # Define questions, options, and correct answers
        self.questions = [
            {
                "question": "What is the correct way to create a variable named 'age' with the value 25?",
                "options": ["a) variable age = 25", "b) age = 25", "c) int age = 25", "d) age := 25"],
                "correct_answer": "b"
            },
            {
                "question": "Which of the following is used to add a comment in Python?",
                "options": ["a) //", "b) /* */", "c) #", "d) <!-- -->"],
                "correct_answer": "c"
            },
            {
                "question": "What does the 'len()' function do in Python?",
                "options": ["a) Returns the largest item in an iterable", 
                           "b) Returns the length of an object", 
                           "c) Returns the lowest item in an iterable", 
                           "d) Returns the sum of all items in an iterable"],
                "correct_answer": "b"
            },
            {
                "question": "Which of the following is the correct way to create a list in Python?",
                "options": ["a) list = [1, 2, 3]", "b) list = (1, 2, 3)", "c) list = {1, 2, 3}", "d) list = 1, 2, 3"],
                "correct_answer": "a"
            },
            {
                "question": "What is the output of print(2 ** 3)?",
                "options": ["a) 6", "b) 5", "c) 8", "d) Error"],
                "correct_answer": "c"
            }
        ]
        
    def display_welcome_message(self):
        """Display a welcome message to the user."""
        print("Welcome to the Python Quiz Bot!")
        print("I'll ask you some beginner-level Python questions.")
        print("Type the letter of your answer (a, b, c, or d).")
        print("Type 'quit' at any time to exit the quiz.")
        print("\nLet's get started!\n")
        
    def ask_question(self):
        """Ask a random question from the question bank."""
        # Select a random question
        question_data = random.choice(self.questions)
        
        # Display the question and options
        print(question_data["question"])
        for option in question_data["options"]:
            print(option)
            
        # Get user's answer
        user_answer = input("\nYour answer: ").lower()
        
        # Check if user wants to quit
        if user_answer == "quit":
            return "quit"
            
        # Check if the answer is correct
        if user_answer == question_data["correct_answer"]:
            print("Correct! Well done!\n")
        else:
            print(f"Sorry, that's incorrect. The correct answer is {question_data['correct_answer']}.\n")
            
        return user_answer
        
    def run(self):
        """Run the quiz bot."""
        self.display_welcome_message()
        
        while True:
            result = self.ask_question()
            if result == "quit":
                print("Thank you for taking the quiz! Goodbye!")
                break
            
            # Ask if they want to continue
            continue_quiz = input("Would you like another question? (yes/no): ").lower()
            if continue_quiz != "yes" and continue_quiz != "y":
                print("Thank you for taking the quiz! Goodbye!")
                break
            print()  # Add a blank line for better readability

if __name__ == "__main__":
    quiz_bot = PythonQuizBot()
    quiz_bot.run()