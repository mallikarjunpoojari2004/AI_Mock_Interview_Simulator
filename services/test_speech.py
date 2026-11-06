
from services.speech_service import transcribe_audio

audio_path = "sample.wav"

with open(audio_path, "rb") as audio_file:
    audio_bytes = audio_file.read()

transcript = transcribe_audio(audio_bytes)

print("\nCandidate's Spoken Answer:")
print(transcript)
