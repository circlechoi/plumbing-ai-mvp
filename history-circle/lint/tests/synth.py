"""테스트용 합성 오디오·영상 생성(numpy + ffmpeg, 크레딧 없음)."""
import os
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SR = 48000
RNG = np.random.default_rng(7)


def tone(dur, db):
    """말소리 대용: RMS가 db(dBFS)인 대역 잡음."""
    n = int(SR * dur)
    x = RNG.standard_normal(n)
    k = np.ones(8) / 8  # 고역을 조금 깎는다
    x = np.convolve(x, k, mode="same")
    return x * (10 ** (db / 20) / (np.sqrt(np.mean(x ** 2)) + 1e-12))


def silence(dur):
    return np.zeros(int(SR * dur))


def write_wav(path, x):
    y = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())


def texture(h, w, seed):
    r = np.random.default_rng(seed)
    f = np.fft.fft2(r.standard_normal((h, w)))
    yy, xx = np.meshgrid(np.fft.fftfreq(h), np.fft.fftfreq(w), indexing="ij")
    f *= 1.0 / (1 + (np.hypot(yy, xx) / 0.02) ** 2)  # 저역 통과 → 부드러운 질감(압축에 강함)
    t = np.real(np.fft.ifft2(f))
    t = (t - t.min()) / (t.max() - t.min())
    return (t * 220 + 18).astype(np.uint8)


def write_video(path, frames, fps=24, audio=None):
    """frames: (N, H, W) uint8 흑백. audio(48k 모노)가 있으면 함께 넣는다."""
    n, h, w = frames.shape
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray", "-s", "%dx%d" % (w, h),
           "-r", str(fps), "-i", "-"]
    tmp = None
    if audio is not None:
        tmp = path + ".a.wav"
        write_wav(tmp, audio)
        cmd += ["-i", tmp, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p", path]
    p = subprocess.run(cmd, input=frames.tobytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if tmp:
        os.remove(tmp)
    if p.returncode:
        raise RuntimeError(p.stderr.decode())


def pan_clip(tex, n, w, h, dx, dy, x0=None, y0=None):
    """큰 질감에서 창을 매 프레임 (dx, dy) 옮겨 자른다 → 화면 내용은 반대(-dx, -dy)로 움직인다."""
    H, W = tex.shape
    x0 = (W - w) // 2 if x0 is None else x0
    y0 = (H - h) // 2 if y0 is None else y0
    out = np.empty((n, h, w), np.uint8)
    for i in range(n):
        x = int(round(x0 + dx * i))
        y = int(round(y0 + dy * i))
        out[i] = tex[y:y + h, x:x + w]
    return out
