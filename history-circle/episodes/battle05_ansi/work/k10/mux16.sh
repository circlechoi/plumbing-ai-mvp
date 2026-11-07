cd ~/ansi/k10
ls seg/s_*.mp4 | sort | sed "s/^/file '/;s/$/'/" > cat.txt
ffmpeg -v error -y -f concat -safe 0 -i cat.txt -i mix16.wav -vf fps=30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -af loudnorm=I=-15:TP=-1.5 -c:a aac -b:a 192k -shortest ansi_anim_v13.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ansi_anim_v13.mp4
