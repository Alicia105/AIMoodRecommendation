from transformers import pipeline
import re
import speech_recognition as sr


# Load the emotion detection model
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

# App responses based on emotion
def emotion_responses_map():
    emotion_responses={
        "joy": {
            "message": "I'm glad you're feeling happy! Let's keep the good vibes going. Here's something upbeat for you.",
            "mood": "happy"
        },
        "sadness": {
            "message": "I'm here for you. Here's something gentle and comforting to help you through.",
            "mood": "sad"
        },
        "anger": {
            "message": "Sounds like it's been a rough time. Let's play something energetic to pass your nerves.",
            "mood": "angry"
        },
        "fear": {
            "message": "It's okay to feel anxious or scared. Let's try something matching your mood to exteriorize everything.",
            "mood": "fearful"
        },
        "surprise": {
            "message": "Whoa! Sounds exciting. Let's keep the energy flowing.",
            "mood": "excited"
        },
        "disgust": {
            "message": "Yikes. Let’s distract you with something relaxing and clean.",
            "mood": "disgust"
        },
        "neutral": {
            "message": "Sounds like today is a chill day ! Let me play something for you ! I got this.",
            "mood": "neutral"
        }
    }
    return emotion_responses

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_emotion(text):
    result = emotion_classifier(text)
    if result and isinstance(result[0], list):  # case: pipeline wrapped in list
        result = result[0]
    emotion = result[0]['label']
    score = result[0]['score']
    return emotion, score

def detection_pipeline(raw_input):
    if raw_input:
        clean_input = preprocess_text(raw_input)
        emotion, score = detect_emotion(clean_input)
        emotion_responses=emotion_responses_map()

        print(f"\n🔍 Detected emotion: {emotion} (confidence: {score:.2f})")
        if emotion in emotion_responses:
            response = emotion_responses[emotion]
            print("\n💬 " + response['message'])
            print(f"🎵 Recommended mood category: {response['mood']}")
        else:
            print("\n🤖 I'm not sure how you're feeling, but here's something neutral.")

