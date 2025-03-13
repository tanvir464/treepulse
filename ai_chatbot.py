from dotenv import load_dotenv
import os
from google import genai
import re

def clean_response(text):
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'[*_]{1,2}(.*?)[*_]{1,2}', r'\1', text)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[\*\-\+]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def generate_gemini_response(content):
    load_dotenv()

    if "API_KEY" not in os.environ:
        print("Warning: API_KEY not found in environment variables.")
        return "I'm unable to access the information at the moment. Please try again later."
    
    try:
        client = genai.Client(api_key=os.environ["API_KEY"])
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=content
        )

        cleaned_response = clean_response(response.text)
        return cleaned_response
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm unable to process your request at the moment. Please try again later."

if __name__ == "__main__":
    query = 'আমার আম গাছে অ্যানথ্রাকনোজ হলে কি করবো?'
    print(generate_gemini_response(query))