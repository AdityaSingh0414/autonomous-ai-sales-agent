import io
import wave

import av


def to_wav_bytes(audio_bytes: bytes) -> bytes:
    pcm = bytearray()
    resampler = av.AudioResampler(
        format="s16",
        layout="mono",
        rate=16000
    )

    with av.open(io.BytesIO(audio_bytes)) as container:
        audio_stream = next(iter(container.streams.audio), None)
        if audio_stream is None:
            raise ValueError("The uploaded file contains no audio stream.")

        for frame in container.decode(audio_stream):
            for converted in resampler.resample(frame):
                pcm.extend(converted.to_ndarray().tobytes())

        for converted in resampler.resample(None):
            pcm.extend(converted.to_ndarray().tobytes())

    if not pcm:
        raise ValueError("The uploaded audio contains no playable samples.")

    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(pcm)

    return output.getvalue()
