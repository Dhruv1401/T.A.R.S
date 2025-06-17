# T.A.R.S. AI Assistant

A modular, voice + text AI assistant for Raspberry Pi 4 powered by claude2-alpaca-7b.Q4_K_M.gguf via llama.cpp, now with simulated emotions.

## 📂 Project Structure

- **engine/**
  - `engine.py`: LLM engine runner + logger
  - `speech_recognition.py`: Microphone input handler
  - `emotion_engine.py`: Random expression/emotion simulation
- **interface/**
  - `text_interface.py`: Terminal-based text input
  - `voice_interface.py`: Text-to-speech output
- **logs/**: Auto-generated chat logs, named `DDMMYYYY.txt`
- **models/**: LLM model file (.gguf)
- **main.py**: Main runtime interface

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
