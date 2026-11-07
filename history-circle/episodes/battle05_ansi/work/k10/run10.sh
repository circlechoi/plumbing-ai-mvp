cd ~/ansi/k10; mkdir -p seg
N=$(python3 -c "import os;exec(open(os.path.expanduser('~/ansi/an/an10.py')).read());print(int(TOTAL*15)+1)")
P=3
for a in $(seq 0 100 $N); do b=$((a+100)); [ $b -gt $N ] && b=$N; f=seg/s_$(printf %05d $a).mp4; [ -f $f.done ] && continue; echo "$a $b"; done > jobs.txt
cat jobs.txt | xargs -P $P -n 2 python3 seg10.py
ls seg/*.done | wc -l
