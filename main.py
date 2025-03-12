from speech_module import speak, listen_for_speech
from image_module import predict_image, process_video
from ai_chatbot import generate_gemini_response

def get_disease_info(disease_name, language):
    """Get description and remedies for the detected disease."""
    if language == 'bn':
        prompt = f"{disease_name} রোগ সম্পর্কে একটি সংক্ষিপ্ত বিবরণ এবং এর প্রতিকার দিন।"
    else:
        prompt = f"Provide a brief description and remedies for {disease_name} disease in mango trees."
    
    response = generate_gemini_response(prompt)
    return response

def main():
    # Ask for language preference via voice
    speak("আপনার ভাষা পছন্দ বলুন। বাংলা বা ইংরেজি?", lang='bn')
    
    # Listen for language choice
    language_choice = listen_for_speech()
    
    # Set language based on user's speech - make Bangla the default
    if language_choice and ('english' in language_choice.lower() or 'ইংরেজি' in language_choice.lower()):
        language = 'en'
        speech_lang = 'en-US'
    else:
        # Default to Bangla even if speech recognition fails
        language = 'bn'
        speech_lang = 'bn-BD'
    
    # Welcome message
    if language == 'bn':
        welcome_msg = "স্বাগতম! আমি আপনার গাছের রোগ নির্ণয়ে সাহায্য করতে এসেছি।"
    else:
        welcome_msg = "Welcome! I'm here to help diagnose diseases in your plants."
    
    print(welcome_msg)
    speak(welcome_msg, lang=language)
    
    # Ask for mode preference
    if language == 'bn':
        mode_msg = "আপনি কি ভিডিও মোড নাকি ফটো মোড ব্যবহার করতে চান? ভিডিও বা ফটো বলুন।"
    else:
        mode_msg = "Would you like to use video mode or photo mode? Please say video or photo."
    
    print(mode_msg)
    speak(mode_msg, lang=language)
    
    # Listen for mode choice
    mode_choice = listen_for_speech(language=speech_lang)
    
    # Process based on mode
    predicted_disease = None
    confidence = 0
    
    if mode_choice and ('video' in mode_choice.lower() or 'ভিডিও' in mode_choice.lower()):
        # Video mode
        if language == 'bn':
            speak("ভিডিও মোড চালু হচ্ছে। আপনার গাছের পাতা ক্যামেরার সামনে ধরুন।", lang=language)
        else:
            speak("Starting video mode. Please show your plant leaf to the camera.", lang=language)
        
        result = process_video(return_result=True)
        if result:
            predicted_disease, confidence = result
    else:
        # Photo mode
        if language == 'bn':
            speak("ফটো মোড চালু হচ্ছে। অনুগ্রহ করে ছবির ফাইলের পথ লিখুন।", lang=language)
        else:
            speak("Starting photo mode. Please enter the path to your image file.", lang=language)
        
        image_path = input("Enter the full path to the image file: ")
        result = predict_image(image_path)
        if result:
            predicted_disease, confidence = result
    
    # Process results and provide information
    if predicted_disease:
        if language == 'bn':
            result_msg = f"আমি {confidence:.2f}% নিশ্চিত যে এটি {predicted_disease} রোগ।"
        else:
            result_msg = f"I am {confidence:.2f}% confident that this is {predicted_disease} disease."
        
        print(result_msg)
        speak(result_msg, lang=language)
        
        # Get disease information and remedies
        disease_info = get_disease_info(predicted_disease, language)
        print(disease_info)
        
        # Ask if the user wants to hear the narration
        if language == 'bn':
            narration_prompt = "আমি কি আপনাকে এই রোগ সম্পর্কে বিস্তারিত বলব? হ্যাঁ বা না বলুন।"
        else:
            narration_prompt = "Would you like me to explain about this disease? Say yes or no."
        
        speak(narration_prompt, lang=language)
        narration_response = listen_for_speech(language=speech_lang)
        
        if narration_response and ('yes' in narration_response.lower() or 'হ্যাঁ' in narration_response.lower()):
            speak(disease_info, lang=language)
    else:
        if language == 'bn':
            no_result_msg = "দুঃখিত, কোন রোগ সনাক্ত করা যায়নি। অনুগ্রহ করে আরও ভালো আলোতে আবার চেষ্টা করুন।"
        else:
            no_result_msg = "Sorry, no disease was detected. Please try again with better lighting."
        
        print(no_result_msg)
        speak(no_result_msg, lang=language)
    
    # Follow-up questions loop
    continue_conversation = True
    while continue_conversation:
        if language == 'bn':
            question_prompt = "আপনার কি আরও কোন প্রশ্ন আছে? যদি থাকে তাহলে জিজ্ঞাসা করুন, অথবা বের হতে 'না' বলুন।"
        else:
            question_prompt = "Do you have any more questions? If yes, please ask, or say 'no' to exit."
        
        print(question_prompt)
        speak(question_prompt, lang=language)
        
        # Listen for question or exit command
        user_response = listen_for_speech(language=speech_lang)
        
        if not user_response or 'no' in user_response.lower() or 'না' in user_response.lower():
            continue_conversation = False
            if language == 'bn':
                farewell = "ধন্যবাদ। আবার দেখা হবে।"
            else:
                farewell = "Thank you. Goodbye!"
            print(farewell)
            speak(farewell, lang=language)
        else:
            # Process the question
            answer = generate_gemini_response(user_response)
            print(answer)
            
            # Directly narrate the response without asking
            print(answer)
            speak(answer, lang=language)
    
    print("Program terminated.")

if __name__ == "__main__":
    main()