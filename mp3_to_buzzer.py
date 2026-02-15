# github.com/OneDevelopmentPL
import argparse
import os
import sys
import numpy as np
from scipy.fft import rfft, rfftfreq
from tqdm import tqdm


import audio.op as audioop
import soundfile as sf


parser = argparse.ArgumentParser(description="MP3 to Arduino/ESP32 Buzzer Converter")
parser.add_argument("--input", required=True, help="Path to input MP3 file")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--arduino", action="store_true", help="Generate for Arduino UNO")
group.add_argument("--esp", action="store_true", help="Generate for ESP32")
parser.add_argument("--chunk", type=int, default=100, help="Chunk size in ms")
parser.add_argument("--minfreq", type=int, default=100, help="Min frequency")
parser.add_argument("--maxfreq", type=int, default=5000, help="Max frequency")
args = parser.parse_args()

if not os.path.exists(args.input):
    print("[ERROR] Input file not found.")
    sys.exit(1)

print("[INFO] Loading audio...")
samples, sample_rate = sf.read(args.input)
samples = np.mean(samples, axis=1)  # mono

print(f"[INFO] Sample rate: {sample_rate} Hz")
chunk_size = int(sample_rate * args.chunk / 1000)

print("[INFO] Starting analysis...")
notes = []
total_chunks = len(samples) // chunk_size

for i in tqdm(range(total_chunks), desc="Processing"):
    start = i * chunk_size
    end = start + chunk_size
    chunk = samples[start:end]

    yf = np.abs(rfft(chunk))
    xf = rfftfreq(len(chunk), 1 / sample_rate)
    freq = xf[np.argmax(yf)]

    if args.minfreq <= freq <= args.maxfreq:
        notes.append((int(freq), args.chunk))
    else:
        notes.append((0, args.chunk))

print("[INFO] Generating generated.ino...")

with open("generated.ino", "w") as f:
    f.write("// Auto-generated buzzer code\n\n")
    if args.arduino:
        f.write("#include <avr/pgmspace.h>\n#define BUZZER_PIN 8\n")
        f.write("const int melody[][2] PROGMEM = {\n")
    else:
        f.write("#define BUZZER_PIN 25\n#define PWM_CHANNEL 0\n#define PWM_FREQ 5000\n#define PWM_RESOLUTION 8\n")
        f.write("int melody[][2] = {\n")
    for freq, dur in notes:
        f.write(f"  {{{freq}, {dur}}},\n")
    f.write("};\n\nint melody_length = " + str(len(notes)) + ";\n\n")

    if args.arduino:
        f.write("""
void setup() {
  for (int i = 0; i < melody_length; i++) {
    int freq = pgm_read_word(&(melody[i][0]));
    int dur = pgm_read_word(&(melody[i][1]));
    if (freq > 0) tone(BUZZER_PIN, freq, dur);
    delay(dur);
    noTone(BUZZER_PIN);
  }
}
void loop() {}
""")
    else:
        f.write("""
void setup() {
  ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(BUZZER_PIN, PWM_CHANNEL);
  for (int i = 0; i < melody_length; i++) {
    int freq = melody[i][0], dur = melody[i][1];
    ledcWriteTone(PWM_CHANNEL, freq > 0 ? freq : 0);
    delay(dur);
  }
}
void loop() {}
""")

print("[SUCCESS] generated.ino created!")
