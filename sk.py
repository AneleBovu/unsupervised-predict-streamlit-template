# sk.py

# Import any necessary libraries
import requests
import json


# Define your functions
def generate_summary(movie_description, api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {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}',
    }

    data = {
        'prompt': movie_description,
        'max_tokens': 150,
        'temperature': 0.7,
        'top_p': 1,
        'n': 1,
        'stop': ['###']
    }

    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data)
    
    print(response.text)  # Print the response for debugging purposes
    
    response_data = json.loads(response.text)
    
    if 'choices' in response_data and len(response_data['choices']) > 0 and 'text' in response_data['choices'][0]:
        return response_data['choices'][0]['text']
    else:
        return "Summary not available"

def main():
    # Main function to execute the script
    api_key = 'your_api_key_here'
    movie_description = "A summary of the movie..."
    summary = generate_summary(movie_description, api_key)
    print(summary)

# Entry point to the script
if __name__ == "__main__":
    main()
