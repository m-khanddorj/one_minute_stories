from typing import List
import random
import glob
import os
import torch

from tts.TTS.api import TTS
from .constants import (
    TTS_CONFIG_PATH,
    TTS_MODEL_PATH,
    TTS_VOICES_PATH
)


def tts(sentences: List[str], output:str) -> List[int]:

    # Get device
    device = device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Init TTS
    tts = TTS(
        model_path=TTS_MODEL_PATH,
        config_path=TTS_CONFIG_PATH,
        progress_bar=False,
    ).to(device)

    wavs = []

    voices = glob.glob(os.path.join(TTS_VOICES_PATH,"*.wav"))
    voice = random.choices(voices)

    for i, sent in enumerate(sentences):
        wav = tts.tts(
            text=sent,
            speaker_wav=voice,
            language="en",
            speed=2
        )
        wavs.append(wav)

    wav = []
    for w in wavs:
        wav += w

    tts.synthesizer.save_wav(wav=wav, path=output, pipe_out=None)
    # Text to speech to a file
    return wavs
