import pyaudio
import wave

def record_audio(duration=5, channels=1, rate=44100, chunk=1024, device_index=6):
    """Function to record audio using PyAudio."""
    p = pyaudio.PyAudio()

    # Set format and initialize stream
    audio_format = pyaudio.paInt16
    frames = []

    stream = p.open(format=audio_format, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk, input_device_index=device_index)

    print("Recording...")
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a .wav file
    with wave.open("output.wav", 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Example usage
if __name__ == "__main__":
    record_audio(duration=5)  # Record for 5 seconds
