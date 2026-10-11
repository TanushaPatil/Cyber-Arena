import wave
import math
import struct

# ============================================================
# CYBER ARENA - THE SILENT IMAGE
# Generates a WAV whose spectrogram contains the hidden flag.
# No NumPy required.
# ============================================================

OUTPUT_FILE = "hidden_audio.wav"

FLAG = "TECH{SILENT_IMAGE}"

# Audio settings
SAMPLE_RATE = 44100
AMPLITUDE = 9000

# Each character is represented using a 5x7 bitmap.
FONT = {
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],

    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],

    "C": [
        "01111",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "01111",
    ],

    "H": [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],

    "{": [
        "01110",
        "01000",
        "01000",
        "11000",
        "01000",
        "01000",
        "01110",
    ],

    "}": [
        "01110",
        "00010",
        "00010",
        "00011",
        "00010",
        "00010",
        "01110",
    ],

    "_": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "11111",
    ],

    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ],

    "I": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "11111",
    ],

    "L": [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ],

    "N": [
        "10001",
        "11001",
        "11001",
        "10101",
        "10011",
        "10011",
        "10001",
    ],

    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],

    "G": [
        "01111",
        "10000",
        "10000",
        "10111",
        "10001",
        "10001",
        "01111",
    ],

    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ],
}


def build_bitmap(text):
    """
    Convert the flag into one large bitmap.
    Each character is 5 pixels wide with one blank column.
    """

    rows = [""] * 7

    for char in text:

        if char not in FONT:
            raise ValueError(f"Character not supported: {char}")

        pattern = FONT[char]

        for row in range(7):
            rows[row] += pattern[row] + "0"

    return rows


def generate_audio(bitmap):
    """
    Convert bitmap pixels into audio tones.

    Each bitmap column becomes a short time segment.
    Each bitmap row corresponds to a different frequency.
    """

    columns = len(bitmap[0])

    # Frequency for each visual row.
    frequencies = [
        900,
        1200,
        1500,
        1800,
        2100,
        2400,
        2700,
    ]

    # Duration of one bitmap column.
    column_duration = 0.055

    samples_per_column = int(SAMPLE_RATE * column_duration)

    audio = []

    for column in range(columns):

        # Find which rows contain a pixel.
        active_rows = []

        for row in range(7):
            if bitmap[row][column] == "1":
                active_rows.append(row)

        for sample in range(samples_per_column):

            t = sample / SAMPLE_RATE

            value = 0.0

            # Combine all active frequencies.
            for row in active_rows:
                frequency = frequencies[row]

                value += math.sin(
                    2 * math.pi * frequency * t
                )

            # Normalize multiple simultaneous tones.
            if active_rows:
                value /= len(active_rows)

            # Slight fade at boundaries.
            fade = 1.0

            fade_samples = int(samples_per_column * 0.08)

            if sample < fade_samples:
                fade = sample / fade_samples

            elif sample > samples_per_column - fade_samples:
                fade = (
                    samples_per_column - sample
                ) / fade_samples

            value *= fade

            sample_value = int(
                value * AMPLITUDE
            )

            audio.append(
                struct.pack("<h", sample_value)
            )

    return b"".join(audio)


def save_wav(audio_data):

    with wave.open(OUTPUT_FILE, "wb") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(audio_data)


def main():

    print("=" * 55)
    print("          CYBER ARENA - THE SILENT IMAGE")
    print("=" * 55)

    print()
    print("Generating spectrogram-hidden audio...")
    print()

    bitmap = build_bitmap(FLAG)

    print("Hidden flag:")
    print(FLAG)

    print()
    print(
        f"Spectrogram width: {len(bitmap[0])} columns"
    )

    audio = generate_audio(bitmap)

    save_wav(audio)

    print()
    print(f"Created: {OUTPUT_FILE}")
    print()
    print("Open the WAV in Sonic Visualiser.")
    print("Enable Spectrogram view.")
    print("The flag will appear in the frequency data.")
    print()
    print("=" * 55)


if __name__ == "__main__":
    main()