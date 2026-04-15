# 🎧 3-Band Audio Equalizer with Real-Time DSP & FFT Visualization

## 📌 Overview
This project is a **desktop-based audio equalizer system** that enables users to dynamically manipulate audio signals using a graphical interface. It implements a **3-band equalizer (Bass, Mid, Treble)** and performs real-time audio processing using Digital Signal Processing (DSP) techniques.

The system also provides **frequency-domain visualization using FFT**, allowing users to observe how different frequency components are affected during processing.

---

## 🚀 Key Features

- 🎚️ 3-Band Equalizer:
  - Bass (Low frequencies: 0–200 Hz)
  - Mid (Vocals: 200–2000 Hz)
  - Treble (High frequencies: 2000+ Hz)

- ⚡ Real-Time Audio Processing
- 🎧 Interactive GUI with dynamic controls
- 🔊 Gain (Volume) Adjustment
- 📊 FFT-based Frequency Spectrum Visualization
- 🔁 Continuous user feedback loop (real-time updates)

---

## 🧠 System Description

The application follows a real-time signal processing pipeline where user input directly influences the audio transformation process.

The user loads a `.wav` file through the GUI, which is then preprocessed by normalizing the signal and converting it to mono format. The audio is passed into a multi-band DSP filter engine where it is decomposed into low, mid, and high frequency components using low-pass, band-pass, and high-pass filters.

Each frequency band is scaled based on user-controlled parameters (bass, mid, treble sliders) and recombined to form the processed signal. Gain adjustment is applied to control amplitude, followed by normalization to prevent clipping.

The processed signal is played back in real time, while FFT-based analysis generates frequency spectrum graphs for both original and processed signals, providing visual validation of the transformation.

---

## 🏗️ System Architecture

The system consists of the following major components:

- **GUI Layer**
  - Handles user interaction (file loading, slider control)

- **Audio Preprocessing**
  - Normalization
  - Stereo to mono conversion

- **Multi-Band DSP Filter Engine**
  - Low-pass filter → Bass extraction
  - Band-pass filter → Mid frequency extraction
  - High-pass filter → Treble extraction
  - Frequency band scaling and recombination

- **Post-Processing**
  - Gain adjustment
  - Signal normalization

- **Real-Time Playback Engine**
  - Streams processed audio output

- **FFT Analysis & Visualization**
  - Converts signal to frequency domain
  - Displays spectrum graphs (original vs processed)

---

## 🔄 Workflow

1. User loads a `.wav` audio file  
2. Audio is preprocessed (normalized and converted to mono)  
3. Signal is split into frequency bands using DSP filters  
4. User adjusts sliders (Bass, Mid, Treble, Gain)  
5. Frequency components are scaled and recombined  
6. Processed audio is played in real time  
7. FFT visualization displays frequency changes  

---

## ▶️ How to Run

```bash
python equalizer.py
