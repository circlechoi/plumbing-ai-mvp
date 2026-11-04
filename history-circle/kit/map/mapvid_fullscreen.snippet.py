import bmap3 as B
B.PANEL = (0, 0, 1080, 1920)   # 반드시 from bmap3 import * · terrain3 · mkbase · mkstyl보다 먼저
from bmap3 import *
import terrain3, mkbase
from mkstyl import masks, highland_from_mask
PANEL = B.PANEL
B.NAT.update({'WAE': (206, 32, 46)}); B.MARK.update({'WAE': '왜'})   # 새 나라는 이렇게 등록
FPS = 15
