import speech_recognition as sr


def get_text_input():
    print("Tell me how you're feeling today:")
    user_input = input(">>> ")
    return user_input


def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Please speak your feelings after the beep...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... (say how you're feeling)")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("😕 Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as e:
        print("⚠️ Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def get_full_user_input():
    print("\nWould you like to (1) Type or (2) Speak your mood?")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "2":
        text = get_speech_input()
        if text:
            return text
        else:
            print("Switching to text input.")
    return get_text_input()

