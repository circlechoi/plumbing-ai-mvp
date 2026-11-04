cd ~ && mkdir -p hs && cd hs && mkdir -p fonts mapdata maps img relief ep
for f in ne_10m_land ne_10m_rivers_lake_centerlines; do [ -f mapdata/$f.geojson ] || curl -sSfL -o mapdata/$f.geojson "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/$f.geojson"; done
[ -f fonts/B.ttf ] || curl -sSfL -o fonts/B.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-Bold.ttf
[ -f fonts/X.ttf ] || curl -sSfL -o fonts/X.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-ExtraBold.ttf
[ -f fonts/SM.ttf ] || curl -sSfL -o fonts/SM.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/songmyung/SongMyung-Regular.ttf
[ -f fonts/NSK.ttf ] || curl -sSfL -o fonts/NSK.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"   # v7.6 제목 = 본고딕 Black(가변 서체, 약 10MB)
[ -f fonts/SEAL.ttf ] || curl -sSfL -o fonts/SEAL.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifkr/NotoSerifKR%5Bwght%5D.ttf"   # 연도 배지 낙관 '史'(약 24MB)
[ -f relief/etopo1.jpg ] || (pip download basemap-data==2.0.0 --no-deps -d /tmp/bm -q && python3 -c "
import zipfile;z=zipfile.ZipFile('/tmp/bm/basemap_data-2.0.0-py3-none-any.whl')
for n in ['etopo1.jpg','shadedrelief.jpg']: open('relief/'+n,'wb').write(z.read('mpl_toolkits/basemap_data/'+n))")
echo READY; sleep 840
