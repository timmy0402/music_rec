import json
import requests
import base64
from difflib import get_close_matches
from typing import Union
from flask import request, Flask

# getting the token and endpoints for Spotify API
API_KEY = "9ea61d2000434f108d05322b9182bfcd"
API_URL = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
#setting flask framework
app = Flask(__name__)

#getting token
def token_getter():
    auth_options = {
    'url': 'https://accounts.spotify.com/api/token',
    'headers': {
        'Authorization': 'Basic ' + base64.b64encode((API_KEY + ':' + '05d158aa10c241d59773219d6ce3a4ca').encode()).decode()
    },
    'form': {
        'grant_type': 'client_credentials'
  }
}   

    response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['form'])
    if response.status_code == 200:
        token = response.json()['access_token']
    return token

#looking for genre TODO
def looking_genre():
    headers = {
        'Authorization' : 'Bearer ' + token_getter()
    }
    response = requests.request("GET",API_URL, headers=headers)
    formatted_response = json.loads((response.text))
    print(formatted_response)
    return formatted_response

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

# Fetch the music recommendations from the Spotify API 
# The music recommendations will be based on the seed artists and the limit
# not working yet
def fetch_music_recommendations(access_token: str, seed_artists: list[str], limit: int) -> list[dict]:
    endpoint = API_URL
    params = {
        'seed_artists': ','.join(seed_artists),
        'limit': limit,
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['tracks']
    else:
        print(f"Failed to fetch recommendations: {response.status_code} - {response.text}")
        return []

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
    token_getter()
    looking_genre()
    chat_bot()
