import json
import requests
from difflib import get_close_matches
from typing import Union

# getting the token and endpoints for Spotify API
API_KEY = "9ea61d2000434f108d05322b9182bfcd"
API_URL = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

# Load the data from the json file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save the knowledge base to the json file
# The data that answer by the user will be saved in the json file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the best match for the user question
def find_best_match(user_question: str, questions: list[str]) -> Union[str, None]:
    
    # get the best match for the user question.                   1 answer, 60% match
    matches: list[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get the answer for the question
def get_answer_for_question(question: str, knowledge_base: dict) -> Union[str, None]:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]


# chat bot function
def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    
    access_token = API_KEY
    
    # The chat bot will keep running until the user types "quit"
    while True:
        user_input: str = input("You: ")
        
        if user_input.lower() == "quit":
            break
        
        # The chat bot will find the best match for the user question
        best_match: Union[str, None] = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])
        
        # If the best match is found, the chat bot will get the answer from the knowledge base
        if best_match:
            answer: Union[str, None] = get_answer_for_question(best_match, knowledge_base)
            print(f'bot: {answer}' if answer else "bot: I don't know the answer.")
        else:
            print('bot: I don\'t know the answer. Can you teach me?')
            
            new_answer: str = input('Type the answer or "skip" to skip: ')
            # If the user types "skip", the chat bot will skip the question
            if new_answer.lower() != "skip":
                # The user question and the answer will be saved in the knowledge base
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('bot: Thank you for teaching me!')

# Run the chat bot
if __name__ == "__main__":
    chat_bot()
