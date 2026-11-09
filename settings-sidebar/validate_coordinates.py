import pathlib, subprocess, tempfile, struct, zlib, collections, sys
from nbt_reader import read
exe = str(pathlib.Path(sys.argv[1]).resolve())
# Distinct tiles expose row/column transposition and vertical inversion.
colors = [(216,127,51),(176,46,38),(22,22,22),(249,255,254),(128,199,31),(60,68,170)]
materials = ['orange_carpet','red_carpet','black_carpet','white_carpet','lime_carpet','blue_carpet']
with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    image = root / 'tiles.png'
    w,h = 384,256
    raw = b''.join(b'\0' + b''.join(bytes(colors[(y//128)*3 + x//128]) for x in range(w)) for y in range(h))
    def chunk(tag,data):
        return struct.pack('>I',len(data)) + tag + data + struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    image.write_bytes(bytes([137,80,78,71,13,10,26,10]) + chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0)) + chunk(b'IDAT',zlib.compress(raw)) + chunk(b'IEND',b''))
    conf = root / 'carpets.conf'
    conf.write_text('MODE(WHITELIST)\n' + '\n'.join('ADD('+c+','+m+')' for c,m in zip(['COLOR_ORANGE','COLOR_RED','COLOR_BLACK','SNOW','COLOR_LIGHT_GREEN','COLOR_BLUE'],materials)))
    output = root / 'North Wall'
    output.mkdir()
    subprocess.run([exe,'--build',str(image),'--format','structure','--output',str(output),'--build-method','flat','--dithering','none','--color-method','euclidean','--color-set',str(conf),'--no-support-blocks','--threads','1','--yes'],check=True)
    expected = {'North Wall '+str(row)+','+str(col)+'.nbt' for row in range(2) for col in range(3)}
    assert {p.name for p in output.glob('*.nbt')} == expected
    for top_row in range(2):
        for column in range(3):
            name = 'North Wall '+str(1-top_row)+','+str(column)+'.nbt'
            data = read(output / name)
            counts = collections.Counter(data['palette'][b['state']]['Name'].replace('minecraft:', '') for b in data['blocks'])
            assert counts.most_common(1)[0][0] == materials[top_row*3+column], (name,counts)
            assert data['size'][0] == 128 and data['size'][2] == 129
    print('Six-map orientation PASS: folder prefix, row 0 at bottom, left-to-right columns, NBT contents match every coordinate')
