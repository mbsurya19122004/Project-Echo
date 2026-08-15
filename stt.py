import argparse
import sys
from pathlib import Path
from chat import ask
from threading import Thread
import sherpa_onnx
import sounddevice as sd

SAMPLE_RATE = 48000
CHUNK_DURATION = 0.1
SAMPLES_PER_READ = int(SAMPLE_RATE * CHUNK_DURATION)

def create_recognizer():
    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens="models/sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25/tokens.txt",
        encoder="models/sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25/encoder.int8.onnx",
        decoder="models/sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25/decoder.int8.onnx",
        joiner="models/sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25/joiner.int8.onnx",
        num_threads=1,
        sample_rate=16000,
        feature_dim=80,
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,  # it essentially disables this rule
        decoding_method="greedy_search",
        provider="cpu",
        # hotwords_file="models/hotwords.txt",
        # hotwords_score=0,
        # blank_penalty=0.0,
        # hr_rule_fsts="",
        # hr_lexicon="",
    )
    return recognizer

def test_STT():
    devices = sd.query_devices()
    if len(devices) == 0:
        print("No microphone devices found")
        sys.exit(0)

    print(devices)
    default_input_device_idx = sd.default.device[0]
    print(f'Use default device: {devices[default_input_device_idx]["name"]}')

    recognizer = create_recognizer()
    print("Started! Please speak")

    # The model is using 16 kHz, we use 48 kHz here to demonstrate that
    # sherpa-onnx will do resampling inside.
    sample_rate = 48000
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms

    stream = recognizer.create_stream()

    display = sherpa_onnx.Display()

    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)  # a blocking read
            samples = samples.reshape(-1)
            stream.accept_waveform(sample_rate, samples)
            while recognizer.is_ready(stream):
                recognizer.decode_stream(stream)

            is_endpoint = recognizer.is_endpoint(stream)

            result = recognizer.get_result(stream)

            display.update_text(result)
            display.display()

            if is_endpoint:
                if result:
                    display.finalize_current_sentence()
                    display.display()

                recognizer.reset(stream)


def get_input_device():
    device_idx = sd.default.device[0]

    if device_idx is None or device_idx < 0:
        print("No default microphone found")
        sys.exit(1)

    device = sd.query_devices(device_idx)

    print(f"Using microphone: {device['name']}")

    return device_idx


def create_audio_stream(device_idx):
    return sd.InputStream(
        device=device_idx,
        channels=1,
        dtype="float32",
        samplerate=SAMPLE_RATE,
        blocksize=SAMPLES_PER_READ,
    )


def read_audio(audio_stream):
    samples, overflowed = audio_stream.read(SAMPLES_PER_READ)

    if overflowed:
        print("Warning: audio buffer overflow")

    return samples.reshape(-1)


def feed_audio(recognizer, stream, samples):
    stream.accept_waveform(SAMPLE_RATE, samples)


def decode_audio(recognizer, stream):
    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

def get_result(recognizer, stream):
    if not recognizer.is_endpoint(stream):
        return None

    result = recognizer.get_result(stream)

    recognizer.reset(stream)

    return result

def handle_result(result):
    if not result:
        return

    print("User:", result)

    Thread(
        target=ask,
        args=(result,),
        daemon=True
    ).start()


def start():
    device_idx = get_input_device()

    recognizer = create_recognizer()
    stream = recognizer.create_stream()

    print("Started! Please speak")

    with create_audio_stream(device_idx) as audio_stream:

        while True:
            samples = read_audio(audio_stream)

            feed_audio(
                recognizer,
                stream,
                samples
            )

            decode_audio(
                recognizer,
                stream
            )

            result = get_result(
                recognizer,
                stream
            )

            handle_result(result)

if __name__ == "__main__":
    try:
        test_STT()
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
