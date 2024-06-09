import whisper
import numpy as np
from pydub import AudioSegment
import torchaudio

def transcribe_with_timestamps(wav_path):
    # Load the whisper model
    model = whisper.load_model("base")
    
    # Load audio
    audio = AudioSegment.from_wav(wav_path)
    
    # Whisper expects a numpy array with a specific sample rate
    audio = audio.set_frame_rate(16000)
    audio_samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    
    # Get the duration of the audio
    duration = len(audio_samples) / 16000.0  # since we set frame rate to 16000
    
    # Transcribe audio with word-level timestamps
    result = model.transcribe(audio_samples, language="en", word_timestamps=True)
    
    # Extract words and their timestamps
    words_with_timestamps = []
    for segment in result['segments']:
        for word in segment['words']:
            words_with_timestamps.append({
                'word': word['word'],
                'start_time': word['start'],
                'end_time': word['end']
            })
    
    return words_with_timestamps