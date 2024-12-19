import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import messagebox
import threading

# Global variables
oscillators_playing = False
freq1 = 440.0  # Default frequency 1 (Hz)
freq2 = 880.0  # Default frequency 2 (Hz)
duration = 1.0  # Default duration (seconds)
sample_rate = 44100  # Sample rate (Hz)
play_thread = None  # Thread to run the audio playback

# Function to generate sine wave
def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.1):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

# Function to play two oscillators
def play_two_oscillators():
    global oscillators_playing
    if oscillators_playing:
        return

    oscillators_playing = True
    try:
        osc1 = generate_sine_wave(freq1, duration, sample_rate)
        osc2 = generate_sine_wave(freq2, duration, sample_rate)
        stereo_signal = np.vstack((osc1, osc2)).T
        sd.play(stereo_signal, samplerate=sample_rate)
        sd.wait()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        oscillators_playing = False

# Function to start playback
def start():
    global freq1, freq2, duration, play_thread
    try:
        freq1 = float(freq1_entry.get())
        freq2 = float(freq2_entry.get())
        duration = float(duration_entry.get())
        if freq1 <= 0 or freq2 <= 0 or duration <= 0:
            messagebox.showwarning("Input Error", "Please enter positive values for frequency and duration.")
            return
        play_thread = threading.Thread(target=play_two_oscillators)
        play_thread.start()
        update_playing_status(True)
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid input. Please enter valid numeric values.")

# Function to stop playback
def stop():
    global oscillators_playing
    if oscillators_playing:
        oscillators_playing = False
        sd.stop()
        update_playing_status(False)
    else:
        messagebox.showwarning("Warning", "No sound is currently playing.")

# Function to update the play/pause indicator
def update_playing_status(is_playing):
    if is_playing:
        status_label.config(text="Playing...", fg="green")
        start_button.config(state="disabled")
        stop_button.config(state="normal")
    else:
        status_label.config(text="Stopped", fg="red")
        start_button.config(state="normal")
        stop_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Frequency Generator")
root.geometry("400x300")
root.configure(bg="#121212")  # Dark background for Spotify-like look

# Spotify-like color scheme
PRIMARY_COLOR = "#1DB954"  # Spotify Green
SECONDARY_COLOR = "#191414"  # Dark background
TEXT_COLOR = "#FFFFFF"  # White text

# Create labels and input fields
freq1_label = tk.Label(root, text="Frequency 1 (Hz):", bg=SECONDARY_COLOR, fg=TEXT_COLOR)
freq1_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
freq1_entry = tk.Entry(root, bg="#333", fg=TEXT_COLOR, borderwidth=0, font=("Arial", 14), insertbackground='white')
freq1_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
freq1_entry.insert(0, "440.0")

freq2_label = tk.Label(root, text="Frequency 2 (Hz):", bg=SECONDARY_COLOR, fg=TEXT_COLOR)
freq2_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
freq2_entry = tk.Entry(root, bg="#333", fg=TEXT_COLOR, borderwidth=0, font=("Arial", 14), insertbackground='white')
freq2_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
freq2_entry.insert(0, "880.0")

duration_label = tk.Label(root, text="Duration (seconds):", bg=SECONDARY_COLOR, fg=TEXT_COLOR)
duration_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
duration_entry = tk.Entry(root, bg="#333", fg=TEXT_COLOR, borderwidth=0, font=("Arial", 14), insertbackground='white')
duration_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
duration_entry.insert(0, "1.0")

# Create play/pause and stop buttons
start_button = tk.Button(root, text="Start", command=start, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Arial", 14), relief="flat", padx=20, pady=10)
start_button.grid(row=3, column=0, padx=20, pady=20)

stop_button = tk.Button(root, text="Stop", command=stop, bg="#E0E0E0", fg=TEXT_COLOR, font=("Arial", 14), relief="flat", padx=20, pady=10)
stop_button.grid(row=3, column=1, padx=20, pady=20)

stop_button.config(state="disabled")  # Initially disabled

# Status label for playing/stopped text
status_label = tk.Label(root, text="Stopped", bg=SECONDARY_COLOR, fg="red", font=("Arial", 12))
status_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

# Add space between the content and window edges
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
