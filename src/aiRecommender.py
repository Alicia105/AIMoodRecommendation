import tkinter as tk
from tkinter import messagebox
import moodDetectionPipeline
import speech_recognition as sr
import math


class aiRecommender():
    def __init__(self, window):
        self.window = window
        self.window.title("Mood-Based Music Recommender")

        #Canvas for waves
        #self.canvas = tk.Canvas(self.window, bg="#f0f4f7", highlightthickness=0)
        #self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Bring widgets above the canvas
        #self.canvas.lower()

        self.label=tk.Label(self.window, text="Enter your mood / feeling:")
        self.label.pack(pady=10)

        self.entry = tk.Text(self.window, height=4, width=50)
        self.entry.pack()

        tk.Button(self.window, text="Detect Mood", command=self.on_submit).pack(pady=10)
        tk.Button(self.window, text="Speech Input", command=self.on_speech).pack(pady=10)

        self.output_label = tk.Label(self.window, text="", font=("Arial", 14), fg="blue")
        self.output_label.pack(pady=10)

        #To see waves
        """for widget in self.window.winfo_children():
            if widget != self.canvas:
                widget.lift()"""
        
        #self.draw_wave()

    def on_submit(self):
        user_input = self.entry.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter something!")
            return
        
        #clean_input = moodDetectionPipeline.preprocess_text(user_input)
        #emotion, score = moodDetectionPipeline.detect_emotion(clean_input)

        #self.output_label.config(text=f"Detected Emotion: {emotion} ({score:.2f})")
        #print(f"Detected Emotion: {emotion} ({score:.2f})")
        self.backgroundBasedOnText(user_input)
    
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
            self.backgroundBasedOnText(text)

            #clean_input = moodDetectionPipeline.preprocess_text(text)
            #emotion, score = moodDetectionPipeline.detect_emotion(clean_input)
            #self.output_label.config(text=f"Detected Emotion: {emotion} ({score:.2f})")

        except sr.UnknownValueError:
            self.output_label.config(text=f"😕 Sorry, I couldn't understand that.")
            print("😕 Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            self.output_label.config(text=f"⚠️ Could not request results from Google Speech Recognition service; {0}".format(e), fg="red")
            print("⚠️ Could not request results from Google Speech Recognition service; {0}".format(e))
        return None
    
    def backgroundBasedOnText(self, text):
        clean_input = moodDetectionPipeline.preprocess_text(text)
        emotion, score = moodDetectionPipeline.detect_emotion(clean_input)

        self.output_label.config(text=f"🎧 Detected Emotion: {emotion} ({score:.2f})")

        # Optional: change background based on emotion
        emotion_colors = {
            "joy": "#FFF9C4",
            "sadness": "#BBDEFB",
            "anger": "#FFCDD2",
            "love": "#F8BBD0",
            "fear": "#D1C4E9",
            "surprise": "#FFECB3"
        }
        target_color = emotion_colors.get(emotion.lower(), "#f0f4f7")
        print(target_color)

        current_color_name = self.window.cget("bg")  # e.g., "SystemButtonFace"
        print(current_color_name)
        current_color = tk_color_to_hex(self.window,current_color_name)
        print(current_color)
        self.animate_background(current_color, target_color)

        """color = emotion_colors.get(emotion.lower(), "#f0f4f7")
        self.window.configure(bg=color)
        self.output_label.configure(bg=color)
        self.label.configure(bg=color)"""

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def animate_background(self, start_color, end_color, steps=20, delay=30):
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)

        def step(i):
            if i > steps:
                return
            current_rgb = tuple(
                int(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * i / steps)
                for j in range(3)
            )
            hex_color = self.rgb_to_hex(current_rgb)
            self.window.configure(bg=hex_color)
            self.output_label.configure(bg=hex_color)
            self.label.configure(bg=hex_color)
            self.window.after(delay, lambda: step(i + 1))

        step(0)

    def blend_colors(bg_rgb, fg_rgb, alpha=0.5):
        """Blend foreground color into background color with alpha (0.0 to 1.0)."""
        return tuple(
            int(bg_rgb[i] * (1 - alpha) + fg_rgb[i] * alpha)
            for i in range(3)
        )
    
def get_rgb_255(widget, color_name):
        """Returns (R, G, B) in 0–255 range from a Tkinter color name."""
        r, g, b = widget.winfo_rgb(color_name)
        return (r // 256, g // 256, b // 256)

def tk_color_to_hex(widget, color_name):
    r, g, b = widget.winfo_rgb(color_name)
    return "#{:02x}{:02x}{:02x}".format(r // 256, g // 256, b // 256)


def main():
    # GUI setup
    root = tk.Tk()
    recommender=aiRecommender(root)
    root.mainloop()

if __name__ == "__main__":
    main()