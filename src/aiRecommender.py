import tkinter as tk
from tkinter import messagebox
import moodDetectionPipeline
import moodInput
import speech_recognition as sr
import math
import interaction

class aiRecommender():
    def __init__(self, window):
        self.user_input=""
        self.emotion=""
        self.emotion_response_map=moodDetectionPipeline.emotion_responses_map()

        self.window = window
        self.window.title("Mood-Based Music Recommender")

        #Canvas for waves
        self.canvas = tk.Canvas(self.window, bg="#f0f4f7", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
       
        self.label=tk.Label(self.window, text="Enter your mood / feeling:")
        self.label.pack(pady=10)

        self.entry = tk.Text(self.window, height=4, width=50)
        self.entry.pack()

        tk.Button(self.window, text="Detect Mood", command=self.on_submit).pack(pady=10)
        tk.Button(self.window, text="Speech Input", command=self.on_speech).pack(pady=10)
        tk.Button(self.window, text="Play music", command=self.on_play_music_mood).pack(pady=10)
        tk.Button(self.window, text="Generate playlist", command=self.on_generate_music).pack(pady=10)
        
        self.output_label = tk.Label(self.window, text="", font=("Arial", 14), fg="blue")
        self.output_label.pack(pady=10)

        #To see waves
        for widget in self.window.winfo_children():
            if widget != self.canvas:
                widget.lift()
        
        self.window.update()  # Let Tkinter compute the window size
        self.draw_wave()
        #self.phase=0
        #self.animate_wave()

        self.phases = [0, 0, 0]
        self.animate_waves()

    def on_submit(self):
        self.user_input = self.entry.get("1.0", tk.END).strip()
        #self.user_input=user_input
        if not self.user_input:
            messagebox.showwarning("Warning", "Please enter something!")
            return
        
        #clean_input = moodDetectionPipeline.preprocess_text(user_input)
        #emotion, score = moodDetectionPipeline.detect_emotion(clean_input)

        #self.output_label.config(text=f"Detected Emotion: {emotion} ({score:.2f})")
        #print(f"Detected Emotion: {emotion} ({score:.2f})")
        self.backgroundBasedOnText()
    
    def on_speech(self):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            # Calibrate for ambient noise
            self.output_label.config(text="🎤 Calibrating for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Prompt user
            moodInput.beep()
            self.output_label.config(text="🎤 Please speak your feelings after the beep...")
            self.window.update()  # Refresh UI before listening
            print("Listening... (say how you're feeling)")
          
            try :
                # Listen with timeout
                audio = recognizer.listen(source, timeout=8)

            except sr.WaitTimeoutError:

                self.output_label.config(text="⌛ Listening timed out. Try again.", fg="red")
                print("⌛ Listening timed out.")
                return
        try:
            # Recognize speech
            text = recognizer.recognize_google(audio)
            print("🗣️ You said:", text)

            self.output_label.config(text=f"🗣️ You said:{text}")
            self.backgroundBasedOnText(text)

        except sr.UnknownValueError:
            self.output_label.config(text=f"😕 Sorry, I couldn't understand that.")
            print("😕 Sorry, I couldn't understand that.")
            return
        except sr.RequestError as e:
            error_message = f"⚠️ Could not request results from Google Speech Recognition service; {e}"
            self.output_label.config(text=error_message, fg="red")
            print("⚠️ Could not request results from Google Speech Recognition service; {0}".format(e))
        return
        
    def on_play_music_mood(self):
        if not self.user_input:
            messagebox.showwarning("Warning", "Please enter something first!")
            return
        else :
            #pipeline to play 5 songs
            messagebox.showwarning("Success", f"We generated a preview of 5 songs matching your current mood : {self.emotion} ! Enjoy !\n You can generate a playlist too if you want ")
            return
        
    def on_generate_music(self):
        if not self.user_input:
            messagebox.showwarning("Warning", "Please enter something first!")
            return
        else :
            #pipeline to create playlist with spotify api
            name=interaction.generate_playlist(self.emotion)
            messagebox.showwarning("Success", f"Your playlist {name} based on {self.emotion} was successfully created !\n You can listen to it on your Spotify app")
            return

    def backgroundBasedOnText(self):
        clean_input = moodDetectionPipeline.preprocess_text(self.user_input)
        self.emotion, score = moodDetectionPipeline.detect_emotion(clean_input)

        self.output_label.config(text=f"🎧 Detected Emotion: {self.emotion} ({score:.2f})")

       
        self.output_label.config(text=f"{self.emotion_response_map[self.emotion]["message"]}")
        # Optional: change background based on emotion
        emotion_colors = {
            "joy": "#FFF9C4",
            "sadness": "#BBDEFB",
            "anger": "#FFCDD2",
            "love": "#F8BBD0",
            "fear": "#D1C4E9",
            "surprise": "#FFECB3"
        }
        target_color = emotion_colors.get(self.emotion.lower(), "#f0f4f7")
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
            #self.window.configure(bg=hex_color)
            self.canvas.configure(bg=hex_color)
            self.output_label.configure(bg=hex_color)
            self.label.configure(bg=hex_color)
            #self.window.after(delay, lambda: step(i + 1))
            self.canvas.after(delay, lambda: step(i + 1))

        step(0)

    def draw_wave(self):
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        if width <= 1 or height <= 1:
            # wait until window is fully initialized
            self.window.after(100, self.draw_wave)
            return

        self.canvas.delete("wave")  # Clear previous waves

        wave_height = 40
        wave_length = 100
        num_points = width // 10

        points1 = []
        for x in range(num_points):
            px = x * 10
            py = int(height / 2 + wave_height * math.sin(2 * math.pi * px / wave_length))
            points1.extend([px, py])

        if len(points1) >= 4:
            self.canvas.create_line(points1, fill="#64b5f6", width=3, tags="wave", smooth=1)

    def animate_wave(self):
        self.canvas.delete("wave")  # Clear previous frame

        width = self.window.winfo_width()
        height = self.window.winfo_height()
        amplitude = 20
        frequency = 0.05

        self.phase += 0.1  # Animate by shifting phase
        points = []
        for x in range(0, width, 5):
            y = height // 2 + int(amplitude * math.sin(frequency * x + self.phase))
            points.extend([x, y])

        self.canvas.create_line(points, fill="#90CAF9", width=3, tags="wave", smooth=1)
        self.window.after(30, self.animate_wave)  # call again after 30ms
    
    def animate_waves(self):
        self.canvas.delete("wave")  # Clear previous waves

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        wave_params = [
            {"amplitude": 20, "frequency": 0.03, "phase_offset": 0, "speed": 0.1, "color": "#90CAF9"},
            {"amplitude": 15, "frequency": 0.035, "phase_offset": 1, "speed": 0.07, "color": "#64B5F6"},
            {"amplitude": 10, "frequency": 0.04, "phase_offset": 2, "speed": 0.05, "color": "#42A5F5"},
        ]

        # Get the background color of the canvas
        background_color = self.window.cget("bg")
        background_hex = tk_color_to_hex(self.window,background_color)
        try:
            bg_rgb =self.hex_to_rgb(background_hex)
        except ValueError:
            bg_rgb = (240, 244, 247)  # Default fallback

        # Draw each wave with color blending
        for idx, wave in enumerate(wave_params):
            self.phases[idx] += wave["speed"]
            points = []
            for x in range(0, width, 5):
                y = height//2 + int(wave["amplitude"] * math.sin(wave["frequency"] * x + self.phases[idx] + wave["phase_offset"]))
                points.extend([x, y])

            # Convert the wave color and blend with background
            wave_rgb = self.hex_to_rgb(wave["color"])
            blended_rgb = blend_colors(bg_rgb, wave_rgb, alpha=0.5)  # You can change alpha to control blending
            blended_color = self.rgb_to_hex(blended_rgb)

            # Draw wave with blended color
            self.canvas.create_line(points, fill=blended_color, width=2, tags="wave", smooth=1)

        # Repeat the animation
        self.window.after(30, self.animate_waves)

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