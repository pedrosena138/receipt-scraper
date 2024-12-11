# type: ignore
import os
import urllib
import urllib.request

import pydub
import speech_recognition as sr

audios_dir = os.path.join(os.getcwd(), "audios")
pydub.AudioSegment.ffmpeg = os.path.join(os.getcwd(), "ffmpeg")


def speech_to_text(source: str) -> str:
    """
    Decode audio into text\n
    # Args
        source: str - source URL for download the audio file
    # Return
        str
    """

    def clean() -> None:
        """Remove audio files from the directory"""
        for file in os.listdir(audios_dir):
            if file.endswith(".mp3") or file.endswith(".wav"):
                os.remove(os.path.join(audios_dir, file))

    filepath = os.path.join(audios_dir, "audio.mp3")
    urllib.request.urlretrieve(source, filepath)

    sound = pydub.AudioSegment.from_mp3(filepath)

    filepath = os.path.join(audios_dir, "audio.wav")
    sound.export(filepath, format="wav")

    sample_audio = sr.AudioFile(filepath)
    recognizer = sr.Recognizer()
    with sample_audio as audio_src:
        audio = recognizer.record(audio_src)

    text: str = recognizer.recognize_google(audio)
    clean()

    return text


__all__ = ["speech_to_text"]
