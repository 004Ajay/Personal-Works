import whisper

AUDIO_FILE="audio.ogg"

model = whisper.load_model("large", device="cpu")  # model sizes - tiny, base, small, medium, large

result = model.transcribe(AUDIO_FILE, language="en")

print(result["text"])
