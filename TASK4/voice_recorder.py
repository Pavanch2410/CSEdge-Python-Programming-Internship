import pyaudio
import wave
import soundfile as sf
import numpy as np

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def list_audio_devices():
    audio = pyaudio.PyAudio()
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        device_info = audio.get_device_info_by_host_api_device_index(0, i)
        print(f"Device {i}: {device_info.get('name')}")
        print(f" - Max Input Channels: {device_info.get('maxInputChannels')}")
        print(f" - Max Output Channels: {device_info.get('maxOutputChannels')}")
    audio.terminate()

def record_audio(seconds, output_file, input_device_index=None):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=input_device_index)
    
    print(f"Recording for {seconds} seconds...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(file, output_device_index=None):
    audio = pyaudio.PyAudio()
    try:
        wf = wave.open(file, 'rb')
    except wave.Error as e:
        print(f"Error opening wave file: {e}")
        return

    channels = wf.getnchannels()
    rate = wf.getframerate()
    width = wf.getsampwidth()

    print(f"Playing audio: channels={channels}, rate={rate}, width={width}")

    def open_stream(output_device_index):
        try:
            return audio.open(format=audio.get_format_from_width(width),
                              channels=1,  # Force to mono
                              rate=rate,
                              output=True,
                              output_device_index=output_device_index)
        except OSError as e:
            print(f"Error opening stream on device {output_device_index}: {e}")
            return None

    stream = open_stream(output_device_index)
    if not stream and output_device_index is not None:
        print("Retrying with default output device...")
        stream = open_stream(None)

    if not stream:
        wf.close()
        audio.terminate()
        return

    data = wf.readframes(CHUNK)
    while data:
        # If the file has more than one channel, convert it to mono
        if channels > 1:
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_data = audio_data.reshape(-1, channels)
            audio_data = audio_data.mean(axis=1, dtype=np.int16)
            data = audio_data.tobytes()
        stream.write(data)
        data = wf.readframes(CHUNK)
    
    stream.stop_stream()
    stream.close()
    wf.close()
    audio.terminate()

def save_audio(input_file, output_file, output_format):
    data, samplerate = sf.read(input_file)
    sf.write(output_file, data, samplerate, format=output_format)
    print(f"File saved as {output_file} in {output_format} format.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Voice Recording Application")
    parser.add_argument('action', choices=['record', 'play', 'save', 'list'], help="Action to perform")
    parser.add_argument('--seconds', type=int, help="Duration of recording in seconds")
    parser.add_argument('--file', type=str, help="File to play or save")
    parser.add_argument('--output', type=str, help="Output file name")
    parser.add_argument('--format', type=str, help="Output file format (e.g., FLAC, OGG, WAV)")
    parser.add_argument('--input_device', type=int, help="Input device index")
    parser.add_argument('--output_device', type=int, help="Output device index")

    args = parser.parse_args()

    if args.action == 'list':
        list_audio_devices()
    
    elif args.action == 'record':
        if args.seconds and args.output:
            record_audio(args.seconds, args.output, input_device_index=args.input_device)
        else:
            print("Please provide the duration (in seconds) and output file name for recording.")
    
    elif args.action == 'play':
        if args.file:
            play_audio(args.file, output_device_index=args.output_device)
        else:
            print("Please provide the file name to play.")
    
    elif args.action == 'save':
        if args.file and args.output and args.format:
            save_audio(args.file, args.output, args.format)
        else:
            print("Please provide the input file name, output file name, and output format for saving.")
