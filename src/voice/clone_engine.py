import ntpath
import os.path
import time
import torch

from TTS.api import TTS
from settings import BASE_DIR


class VoiceCloner:
    def __init__(self):
        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # List available 🐸TTS models
        # print(TTS().list_models())
        # Init TTS
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    def run(self, speaker_wav, text):
        # Run TTS
        # ❗ Since this model is multilingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        st_time = time.time()
        output_path = os.path.join(BASE_DIR,
                                   f"{ntpath.basename(speaker_wav).replace('.wav', '')}_output.wav")
        # Text to speech to a file
        self.tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=output_path)
        print(f"Processing Time: {time.time() - st_time}")

        return output_path


if __name__ == '__main__':
    voice_cloner = VoiceCloner()
    for i in range(3):
        voice_cloner.run(text="", speaker_wav="")
