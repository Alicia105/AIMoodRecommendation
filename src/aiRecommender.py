import tkinter as tk
from tkinter import messagebox
import moodDetectionPipeline
import speech_recognition as sr

class aiRecommender():
    def __init__(self, window):
        self.window = window
        self.window.title("Mood-Based Music Recommender")

        label=tk.Label(self.window, text="Enter your mood / feeling:")
        label.pack(pady=10)

        self.entry = tk.Text(self.window, height=4, width=50)
        self.entry.pack()

        tk.Button(self.window, text="Detect Mood", command=self.on_submit).pack(pady=10)
        tk.Button(self.window, text="Speech Input", command=self.on_speech).pack(pady=10)

        self.output_label = tk.Label(self.window, text="", font=("Arial", 14), fg="blue")
        self.output_label.pack(pady=10)


    def on_submit(self):
        user_input = self.entry.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter something!")
            return
        
        clean_input = moodDetectionPipeline.preprocess_text(user_input)
        emotion, score = moodDetectionPipeline.detect_emotion(clean_input)

        self.output_label.config(text=f"Detected Emotion: {emotion} ({score:.2f})")
        print(f"Detected Emotion: {emotion} ({score:.2f})")
    
    def on_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Please speak your feelings after the beep...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening... (say how you're feeling)")
            self.output_label.config(text=f"🎤 Please speak your feelings after the beep...")
            self.output_label.config(text=f"Listening... (say how you're feeling)")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("🗣️ You said:", text)
            self.output_label.config(text=f"🗣️ You said:{text}")

            clean_input = moodDetectionPipeline.preprocess_text(text)
            emotion, score = moodDetectionPipeline.detect_emotion(clean_input)
            self.output_label.config(text=f"Detected Emotion: {emotion} ({score:.2f})")

        except sr.UnknownValueError:
            self.output_label.config(text=f"😕 Sorry, I couldn't understand that.")
            print("😕 Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            self.output_label.config(text=f"⚠️ Could not request results from Google Speech Recognition service; {0}".format(e), fg="red")
            print("⚠️ Could not request results from Google Speech Recognition service; {0}".format(e))
        return None
    
   

def main():
    # GUI setup
    root = tk.Tk()
    recommender=aiRecommender(root)
    root.mainloop()

if __name__ == "__main__":
    main()