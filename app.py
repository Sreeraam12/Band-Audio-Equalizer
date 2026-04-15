import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# =========================
# GLOBAL VARIABLES
# =========================
audio = None
sr = None
is_playing = False

# =========================
# LOAD AUDIO
# =========================
def load_audio():
    global audio, sr
    
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    
    if file_path:
        sr, audio_data = wav.read(file_path)

        audio_data = audio_data.astype(np.float32)

        # Normalize
        audio_data = audio_data / np.max(np.abs(audio_data))

        # Stereo → Mono
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        audio = audio_data
        status_label.config(text="Audio Loaded!")

# =========================
# FILTERS
# =========================
def low_pass(data, cutoff, sr):
    b, a = butter(4, cutoff/(sr/2), btype='low')
    return lfilter(b, a, data)

def high_pass(data, cutoff, sr):
    b, a = butter(4, cutoff/(sr/2), btype='high')
    return lfilter(b, a, data)

def band_pass(data, low, high, sr):
    b, a = butter(4, [low/(sr/2), high/(sr/2)], btype='band')
    return lfilter(b, a, data)

# =========================
# PROCESS AUDIO
# =========================
def process_audio():
    global audio, sr

    if audio is None:
        return None

    bass = bass_slider.get()
    mid = mid_slider.get()
    treble = treble_slider.get()
    gain = gain_slider.get()

    low_part = low_pass(audio, 200, sr)
    mid_part = band_pass(audio, 200, 2000, sr)
    high_part = high_pass(audio, 2000, sr)

    processed = (
        audio +
        low_part * (bass * 0.5) +
        mid_part * (mid * 0.5) +
        high_part * (treble * 0.5)
    )

    processed = processed * (1 + gain * 0.2)

    processed = processed / np.max(np.abs(processed))

    return processed

# =========================
# VISUAL PROOF (FFT)
# =========================
def show_spectrum(signal, sr, title="Spectrum"):
    fft = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(fft), 1/sr)

    plt.figure()
    plt.plot(freq[:len(freq)//2], np.abs(fft)[:len(fft)//2])
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

# =========================
# PLAY AUDIO
# =========================
def play_audio():
    global is_playing

    if audio is None:
        status_label.config(text="Load audio first!")
        return

    processed = process_audio()

    if processed is not None:
        sd.stop()
        sd.play(processed, sr)
        is_playing = True
        status_label.config(text="Playing...")

        # Show visual proof
        show_spectrum(audio, sr, "Original Spectrum")
        show_spectrum(processed, sr, "Processed Spectrum")

# =========================
# STOP AUDIO
# =========================
def stop_audio():
    global is_playing
    sd.stop()
    is_playing = False
    status_label.config(text="Stopped")

# =========================
# REAL-TIME UPDATE
# =========================
def update_audio(event=None):
    if is_playing:
        play_audio()

# =========================
# GUI (ENHANCED)
# =========================
root = tk.Tk()
root.title("🎧 3-Band Audio Equalizer")
root.geometry("420x550")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="3-Band Audio Equalizer",
                 font=("Arial", 18, "bold"),
                 fg="white", bg="#1e1e1e")
title.pack(pady=15)

load_btn = tk.Button(root, text="Load Audio (.wav)",
                     command=load_audio,
                     bg="#3a86ff", fg="white",
                     font=("Arial", 11, "bold"),
                     width=20)
load_btn.pack(pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

def create_slider(label_text):
    frame_inner = tk.Frame(frame, bg="#1e1e1e")
    frame_inner.pack(pady=8)

    label = tk.Label(frame_inner, text=label_text,
                     fg="white", bg="#1e1e1e",
                     font=("Arial", 11))
    label.pack()

    value_label = tk.Label(frame_inner, text="0",
                           fg="#00ffcc", bg="#1e1e1e",
                           font=("Arial", 10, "bold"))
    value_label.pack()

    slider = tk.Scale(frame_inner,
                      from_=0, to=10,
                      orient=tk.HORIZONTAL,
                      length=250,
                      bg="#1e1e1e",
                      fg="white",
                      highlightthickness=0,
                      troughcolor="#444",
                      command=lambda val: update_slider(val, value_label))
    slider.pack()

    return slider

def update_slider(val, label):
    label.config(text=str(val))
    update_audio()

bass_slider = create_slider("Bass (Low)")
mid_slider = create_slider("Mid (Vocals)")
treble_slider = create_slider("Treble (High)")
gain_slider = create_slider("Gain (Volume)")

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)

play_btn = tk.Button(btn_frame, text="▶ Play",
                     command=play_audio,
                     bg="#06d6a0", fg="black",
                     font=("Arial", 12, "bold"),
                     width=10)
play_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(btn_frame, text="■ Stop",
                     command=stop_audio,
                     bg="#ef476f", fg="white",
                     font=("Arial", 12, "bold"),
                     width=10)
stop_btn.grid(row=0, column=1, padx=10)

status_label = tk.Label(root,
                        text="Load a .wav file",
                        fg="#00ffcc",
                        bg="#1e1e1e",
                        font=("Arial", 11))
status_label.pack(pady=15)

root.mainloop()
