"""검사 공통 도구: 임계값 읽기, ffmpeg 디코드, RMS, 결과 출력."""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
THRESHOLDS_PATH = os.environ.get("HC_LINT_THRESHOLDS", os.path.join(HERE, "thresholds.json"))

AUDIO_SR = 16000


def th(check, key):
    """thresholds.json에서 값 하나를 읽는다."""
    with open(THRESHOLDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data[check][key]["value"]


def result(check, ok, violations=None, metrics=None, warnings=None, target=None):
    return {
        "check": check,
        "target": target,
        "ok": bool(ok),
        "violations": violations or [],
        "warnings": warnings or [],
        "metrics": metrics or {},
    }


def emit(res):
    """CLI 공통 출력: JSON을 찍고 실패면 exit 1."""
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res["ok"] else 1)


def _run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("명령 실패: %s\n%s" % (" ".join(cmd), p.stderr.decode("utf-8", "replace")[-2000:]))
    return p


# ---------- 오디오 ----------

def load_audio(path, sr=AUDIO_SR):
    """모노 float32 [-1,1] 배열로 읽는다(영상 파일이면 오디오 트랙)."""
    p = _run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(p.stdout, dtype=np.float32).copy()


def rms_db_frames(x, sr=AUDIO_SR, frame_s=0.01):
    """프레임별 RMS(dBFS). 반환: (dB 배열, 프레임 길이 초)."""
    n = max(1, int(round(sr * frame_s)))
    m = len(x) // n
    if m == 0:
        return np.array([-120.0]), frame_s
    fr = x[: m * n].reshape(m, n).astype(np.float64)
    r = np.sqrt(np.mean(fr * fr, axis=1))
    return 20 * np.log10(r + 1e-10), n / sr


def segments(mask, frame_s):
    """불리언 프레임 마스크의 연속 True 구간 [(start_s, end_s), ...]."""
    segs = []
    m = np.concatenate([[False], np.asarray(mask, bool), [False]])
    d = np.diff(m.astype(np.int8))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    for s, e in zip(starts, ends):
        segs.append((s * frame_s, e * frame_s))
    return segs


def integrated_lufs(path):
    """ffmpeg ebur128 필터로 통합 라우드니스(LUFS)."""
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    err = p.stderr.decode("utf-8", "replace")
    m = re.findall(r"I:\s*(-?[\d.]+|-inf)\s*LUFS", err)
    if not m:
        raise RuntimeError("ebur128 결과를 읽지 못함: " + err[-800:])
    v = m[-1]
    return float("-inf") if v == "-inf" else float(v)


# ---------- 영상 ----------

def probe_size(path):
    p = _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
              "-of", "csv=p=0:s=x", path])
    w, h = p.stdout.decode().strip().split("x")[:2]
    return int(w), int(h)


def load_gray_frames(path, fps, width=160):
    """fps로 표본 추출한 축소 흑백 프레임 (N, H, W) float32."""
    w0, h0 = probe_size(path)
    h = max(2, int(round(h0 * width / w0 / 2)) * 2)
    p = _run(["ffmpeg", "-v", "error", "-i", path, "-vf", "fps=%g,scale=%d:%d,format=gray" % (fps, width, h),
              "-f", "rawvideo", "-"])
    buf = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(buf) // (width * h)
    return buf[: n * width * h].reshape(n, h, width).astype(np.float32)


def frame_diffs(frames):
    if len(frames) < 2:
        return np.zeros(0)
    return np.mean(np.abs(np.diff(frames, axis=0)), axis=(1, 2))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
