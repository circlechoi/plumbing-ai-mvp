"""효과음 트랙이 내레이션보다 커지는 구간 검사.

사용: python3 audio_sfx_vs_vo.py vo.wav sfx.wav
같은 구간(window_s)에서 내레이션이 말하고 효과음도 울릴 때,
효과음 RMS > 내레이션 RMS − margin_db 이면 실패.
근거: history-longform:93 '모든 효과음이 내레이션보다 작게'(10/16)
"""
import argparse

import numpy as np

from common import AUDIO_SR, emit, load_audio, result, th

CHECK = "audio_sfx_vs_vo"


def _win_db(x, n):
    m = int(np.ceil(len(x) / n))
    pad = np.zeros(m * n, dtype=np.float64)
    pad[: len(x)] = x
    r = np.sqrt(np.mean(pad.reshape(m, n) ** 2, axis=1))
    return 20 * np.log10(r + 1e-10)


def check(vo_path, sfx_path):
    margin = th(CHECK, "margin_db")
    win = th(CHECK, "window_s")
    vo_on = th(CHECK, "vo_active_db")
    sfx_on = th(CHECK, "sfx_active_db")
    vo = load_audio(vo_path)
    sfx = load_audio(sfx_path)
    L = max(len(vo), len(sfx))
    vo = np.pad(vo, (0, L - len(vo)))
    sfx = np.pad(sfx, (0, L - len(sfx)))
    n = int(AUDIO_SR * win)
    vdb = _win_db(vo, n)
    sdb = _win_db(sfx, n)
    viol = []
    worst = None
    for i, (a, b) in enumerate(zip(vdb, sdb)):
        if a < vo_on or b < sfx_on:
            continue
        over = b - (a - margin)
        worst = over if worst is None else max(worst, over)
        if over > 0:
            viol.append({
                "start_s": round(i * win, 2), "end_s": round((i + 1) * win, 2),
                "vo_rms_db": round(float(a), 1), "sfx_rms_db": round(float(b), 1),
                "over_db": round(float(over), 1),
            })
    return result(CHECK, not viol, viol,
                  {"windows_compared": int(np.sum((vdb >= vo_on) & (sdb >= sfx_on))),
                   "worst_over_db": None if worst is None else round(float(worst), 1),
                   "margin_db": margin}, target=[vo_path, sfx_path])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("vo")
    ap.add_argument("sfx")
    a = ap.parse_args()
    emit(check(a.vo, a.sfx))
