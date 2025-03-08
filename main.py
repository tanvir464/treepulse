from speech_module import speech_to_text, speak
from image_module import predict_image
from ai_chatbot import generate_gemini_response

def generate_introduction(language):
    if language == 'bn':
        return "স্বাগতম! আমি আপনার গাছের রোগ নির্ণয়ে সাহায্য করতে এসেছি।"
    else:
        return "Welcome! I'm here to help diagnose your plant diseases."

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
        predicted_disease, confidence = predict_image(image_path)  # modify to return disease name
    else:
        # Implement process_video() if needed
        predicted_disease = "Anthracnose"  # dummy assignment for illustration
    
    # Generate a detailed response (could be further customized)
    response = f"Predicted Disease: {predicted_disease} with confidence {confidence:.2f}%"
    print("Response:", response)
    speak(response, lang='bn' if language=='bn' else 'en')

if __name__ == "__main__":
    main()