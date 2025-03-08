from dotenv import load_dotenv
import os
from google import genai

def generate_gemini_response(content):
    load_dotenv()
    
    client = genai.Client(api_key=os.environ["API_KEY"])
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=content
    )
    return response.text

# Example usage
if __name__ == "__main__":
    query = 'আমার আম গাছে অ্যানথ্রাকনোজ হলে কি করবো?'
    print(generate_gemini_response(query))
