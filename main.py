from speech_module import speak, listen_for_speech
from image_module import predict_image, process_video
from ai_chatbot import generate_gemini_response

conversation_history = []

def get_gemini_response(new_message):
    global conversation_history
    conversation_history.append("User: " + new_message)
    prompt = "\n".join(conversation_history) + "\nAssistant:"
    response = generate_gemini_response(prompt)
    conversation_history.append("Assistant: " + response)
    return response

def get_disease_info(disease_name, language):
    if language == 'bn':
        prompt = (
            f"আমাদের গাছে {disease_name} রোগ দেখা যাচ্ছে। অনুগ্রহ করে এক অনুচ্ছেদে এই রোগের সংক্ষিপ্ত বিবরণ এবং এর প্রতিকার সম্পর্কে বিস্তারিত জানান।"
        )
    else:
        prompt = (
            f"Our mango tree shows signs of {disease_name} disease. Please provide a brief description and remedies for this disease in one paragraph."
        )
    response = get_gemini_response(prompt)
    return response

def get_language_choice():
    speak("আপনার ভাষা পছন্দ বলুন। বাংলা বা ইংরেজি?", lang='bn')
    while True:
        response = listen_for_speech(language="bn-BD")
        if response is not None:
            lower_resp = response.lower()
            if "english" in lower_resp or "ইংরেজি" in lower_resp:
                return "en", "en-US"
            elif "bangla" in lower_resp or "বাংলা" in lower_resp:
                return "bn", "bn-BD"
        speak("দয়া করে বাংলা বা ইংরেজি বলুন।", lang='bn')

def get_mode_choice(language, speech_lang):
    if language == 'bn':
        speak("আপনি কি ভিডিও মোড নাকি ফটো মোড ব্যবহার করতে চান? ভিডিও বা ফটো বলুন।", lang=language)
    else:
        speak("Would you like to use video mode or photo mode? Please say video or photo.", lang=language)
    while True:
        response = listen_for_speech(language=speech_lang)
        if response is not None:
            lower_resp = response.lower()
            if "video" in lower_resp or "ভিডিও" in lower_resp:
                return "video"
            elif "photo" in lower_resp or "ফটো" in lower_resp:
                return "photo"
        if language == 'bn':
            speak("দয়া করে ভিডিও বা ফটো বলুন।", lang=language)
        else:
            speak("Please say either video or photo.", lang=language)

def get_narration_choice(language, speech_lang):
    if language == 'bn':
        speak("আমি কি আপনাকে এই রোগ সম্পর্কে বিস্তারিত বলব? হ্যাঁ বা না বলুন।", lang=language)
    else:
        speak("Would you like me to explain about this disease? Say yes or no.", lang=language)
    while True:
        response = listen_for_speech(language=speech_lang)
        if response is not None:
            lower_resp = response.lower()
            if "yes" in lower_resp or "হ্যাঁ" in lower_resp:
                return True
            elif "no" in lower_resp or "না" in lower_resp:
                return False
        if language == 'bn':
            speak("দয়া করে হ্যাঁ বা না বলুন।", lang=language)
        else:
            speak("Please say yes or no.", lang=language)

def main():
    global conversation_history
    conversation_history = []

    language, speech_lang = get_language_choice()
    
    if language == 'bn':
        welcome_msg = "স্বাগতম! আমি আপনার গাছের রোগ নির্ণয়ে সাহায্য করতে এসেছি।"
    else:
        welcome_msg = "Welcome! I'm here to help diagnose diseases in your plants."
    print(welcome_msg)
    speak(welcome_msg, lang=language)
    conversation_history.append("Assistant: " + welcome_msg)
    
    mode_choice = get_mode_choice(language, speech_lang)
    
    predicted_disease = None
    confidence = 0
    
    if mode_choice == "video":
        if language == 'bn':
            speak("ভিডিও মোড চালু হচ্ছে। আপনার গাছের পাতা ক্যামেরার সামনে ধরুন।", lang=language)
        else:
            speak("Starting video mode. Please show your plant leaf to the camera.", lang=language)
        result = process_video(return_result=True)
        if result:
            predicted_disease, confidence = result
    else:
        if language == 'bn':
            speak("ফটো মোড চালু হচ্ছে। অনুগ্রহ করে ছবির ফাইলের পথ লিখুন।", lang=language)
        else:
            speak("Starting photo mode. Please enter the path to your image file.", lang=language)
        image_path = input("Enter the full path to the image file: ")
        result = predict_image(image_path)
        if result:
            predicted_disease, confidence = result
    
    if predicted_disease:
        if language == 'bn':
            result_msg = f"আমি {confidence:.2f}% নিশ্চিত যে এটি {predicted_disease} রোগ।"
        else:
            result_msg = f"I am {confidence:.2f}% confident that this is {predicted_disease} disease."
        print(result_msg)
        speak(result_msg, lang=language)
        conversation_history.append("Assistant: " + result_msg)
        
        disease_info = get_disease_info(predicted_disease, language)
        print(disease_info)
        
        narration_choice = get_narration_choice(language, speech_lang)
        if narration_choice:
            speak(disease_info, lang=language)
    else:
        if language == 'bn':
            no_result_msg = "দুঃখিত, কোন রোগ সনাক্ত করা যায়নি। অনুগ্রহ করে আরও ভালো আলোতে আবার চেষ্টা করুন।"
        else:
            no_result_msg = "Sorry, no disease was detected. Please try again with better lighting."
        print(no_result_msg)
        speak(no_result_msg, lang=language)
        conversation_history.append("Assistant: " + no_result_msg)
    
    continue_conversation = True
    while continue_conversation:
        if language == 'bn':
            question_prompt = "আপনার কি আরও কোন প্রশ্ন আছে? যদি থাকে তাহলে জিজ্ঞাসা করুন, অথবা বের হতে 'না' বলুন।"
        else:
            question_prompt = "Do you have any more questions? If yes, please ask, or say 'no' to exit."
        print(question_prompt)
        speak(question_prompt, lang=language)
        
        while True:
            user_response = listen_for_speech(language=speech_lang)
            if user_response is not None:
                break
            if language == 'bn':
                speak("আপনার কোন প্রশ্ন থাকলে জিজ্ঞাসা করুন অথবা বেরিয়ে যেতে না বলুন।", lang=language)
            else:
                speak("Ask if you have any questions or say no to exit.", lang=language)
        
        lower_resp = user_response.lower()
        if 'no' in lower_resp or 'না' in lower_resp:
            continue_conversation = False
            if language == 'bn':
                farewell = "ধন্যবাদ। আবার দেখা হবে।"
            else:
                farewell = "Thank you. Goodbye!"
            print(farewell)
            speak(farewell, lang=language)
            conversation_history.append("Assistant: " + farewell)
        else:
            if language == 'bn':
                user_response = user_response + " একটি অনুচ্ছেদে উত্তর দিন।"
            else:
                user_response = user_response + " Respond within a paragraph."
            answer = get_gemini_response(user_response)
            print(answer)
            speak(answer, lang=language)
    
    print("Program terminated.")

if __name__ == "__main__":
    main()