from dotenv import load_dotenv
import os
from google import genai
import re

def clean_response(text):
    """
    Clean the response text by removing Markdown formatting:
    - Remove # symbols used for headers
    - Remove * or _ symbols used for emphasis
    - Remove numbered list prefixes (1., 2., etc.)
    - Remove bullet points
    - Fix extra newlines
    """
    # Remove Markdown headers (# Header)
    text = re.sub(r'#+\s*', '', text)
    
    # Remove Markdown emphasis (* or _)
    text = re.sub(r'[*_]{1,2}(.*?)[*_]{1,2}', r'\1', text)
    
    # Remove numbered list prefixes but keep the text
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    
    # Remove bullet points but keep the text
    text = re.sub(r'^\s*[\*\-\+]\s*', '', text, flags=re.MULTILINE)
    
    # Fix multiple consecutive newlines (more than 2) to just 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def generate_gemini_response(content):
    """
    Generate a response using Google's Gemini API.
    
    Args:
        content: The query or prompt to send to the model
        
    Returns:
        The cleaned text response from the model
    """
    load_dotenv()
    
    # Check if API key is available
    if "API_KEY" not in os.environ:
        print("Warning: API_KEY not found in environment variables.")
        return "I'm unable to access the information at the moment. Please try again later."
    
    try:
        client = genai.Client(api_key=os.environ["API_KEY"])
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=content
        )
        
        # Clean the response text before returning
        cleaned_response = clean_response(response.text)
        return cleaned_response
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm unable to process your request at the moment. Please try again later."

# Example usage
if __name__ == "__main__":
    query = 'আমার আম গাছে অ্যানথ্রাকনোজ হলে কি করবো?'
    print(generate_gemini_response(query))