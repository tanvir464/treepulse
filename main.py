from speech_module import speech_to_text, speak
from image_module import predict_image
from data_fetcher import fetch_disease_info
from ai_chatbot import generate_introduction

def main():
    # Language mode selection (could be via speech or input)
    language = input("Choose language (en for English, bn for Bangla): ").strip()
    
    # Introduce the bot
    intro = generate_introduction(language)
    print("Bot Introduction:", intro)
    speak(intro, lang='bn' if language=='bn' else 'en')
    
    # Run disease detection (choose mode: photo or video)
    mode = input("Enter 0 for Video Mode or 1 for Photo Mode: ").strip()
    if mode == '1':
        image_path = input("Enter the image file path: ")
        predicted_disease = predict_image(image_path)  # modify to return disease name
    else:
        # Implement process_video() if needed
        predicted_disease = "Anthracnose"  # dummy assignment for illustration
    
    # Fetch disease information from the internet
    disease_info = fetch_disease_info(predicted_disease, lang=language)
    
    # Generate a detailed response (could be further customized)
    response = f"The detected disease is {predicted_disease}. Details: {disease_info}"
    print("Response:", response)
    speak(response, lang='bn' if language=='bn' else 'en')

if __name__ == "__main__":
    main()