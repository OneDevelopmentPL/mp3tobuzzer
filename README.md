# 🎵 mp3tobuzzer

**Convert YouTube or local MP3 audio into Arduino / ESP32 buzzer code.**

This project allows you to download audio from YouTube and convert it into a sequence of frequencies that can be played on a buzzer connected to an Arduino or ESP32.

---

## 🧠 Features

* Download YouTube videos as MP3
* Convert MP3 audio into Arduino/ESP32 compatible buzzer code
* Support for:

  * **Arduino UNO** (PROGMEM)
  * **ESP32** (PWM tone output)
* Progress bar feedback during conversion
* Automatic generation of ready‑to‑use `generated.ino` file

---

## 📁 Project Structure

```
mp3tobuzzer/
├── mp3_to_buzzer.py
├── yt2mp3.py
├── requirements_yt2mp3.txt
├── requirements_mp3tobuzzer.txt
├── generated.ino          # auto‑generated Arduino/ESP32 sketch
└── README.md
```

---

## 🧩 Requirements

### ⚙️ Python

This project requires:

* **Python 3.10 / 3.11 / 3.12**

> ⚠️ Python 3.13+ and 3.14 removed the `audioop` module, which breaks some audio‑related libraries.

---

## 🚀 Installation

### 1️⃣ Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2️⃣ Install dependencies

#### For YouTube downloader (`yt2mp3.py`)

```bash
pip install -r requirements_yt2mp3.txt
```

#### For MP3‑to‑buzzer converter (`mp3_to_buzzer.py`)

```bash
pip install -r requirements_mp3tobuzzer.txt
```

---

## 🔧 System Dependencies

✔ **FFmpeg** — required for audio processing

Install on macOS:

```bash
brew install ffmpeg
```
Install on Arch Linux:
```bash
sudo pacman -S ffmpeg
```
Install on Ubuntu:
```bash
sudo apt install ffmpeg
```

Install on Windows:
```bash
winget install ffmpeg
```

---

## 📥 Usage

### 1️⃣ Download audio from YouTube as MP3

```bash
python yt2mp3.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

This creates a MP3 file in the current directory.

---

### 2️⃣ Convert MP3 to Arduino/ESP32 buzzer code

```bash
python mp3_to_buzzer.py --input yourfile.mp3 --arduino
```

or for ESP32:

```bash
python mp3_to_buzzer.py --input yourfile.mp3 --esp
```

---

## 🧾 Command Options

| Option      | Description                               |
| ----------- | ----------------------------------------- |
| `--input`   | Path to the input MP3 file                |
| `--arduino` | Generate code for Arduino UNO             |
| `--esp`     | Generate code for ESP32                   |
| `--chunk`   | Chunk size in milliseconds (default: 100) |
| `--minfreq` | Minimum frequency threshold               |
| `--maxfreq` | Maximum frequency threshold               |

---

## 📄 Output

The script generates a file called:

```
generated.ino
```

This sketch includes:

* A buzzer pin definition
* A frequency table of tones
* Playback logic
* Memory optimization for Arduino (PROGMEM)
* PWM tone on ESP32

---

## 🛠️ How It Works

1. The MP3 file is split into short chunks (ms based)
2. FFT is applied to detect dominant frequency per chunk
3. Frequencies are translated into buzzer notes
4. Sketch is built with those notes

---

## 📦 Example Flow

```bash
# 1. Download YouTube audio
python yt2mp3.py --url "https://www.youtube.com/watch?v=ynON9o2yHVk"

# 2. Convert MP3 to Arduino code
python mp3_to_buzzer.py --input "Song Title.mp3" --arduino

# 3. Upload `generated.ino` to Arduino or ESP32
```

---

## 🧠 Notes

* This is **not a full MP3 player** — it approximates dominant frequencies into buzzer tones
* Works best with monophonic sound or simple melodies
* ESP32 uses **PWM output** (higher quality than `tone()`)

---

## ❤️ Acknowledgments

Inspired by hobbyist projects converting audio into microcontroller buzzer output.

---

## 📜 License

MIT © OneDevelopment
