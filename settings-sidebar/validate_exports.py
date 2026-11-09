import argparse, pathlib, subprocess, tempfile, struct, zlib
p=argparse.ArgumentParser(); p.add_argument('--source'); p.add_argument('--exe'); a=p.parse_args()
if a.source:
 r=pathlib.Path(a.source)/'src'
 s=(r/'mapart/project.cpp').read_text(); assert s.count('_carpet)')==16 and 'ADD(COLOR_ORANGE,orange_carpet)' in s
 s=(r/'wx/materials_window.cpp').read_text(); assert 'ADD(COLOR_ORANGE,orange_carpet)' in s
 s=(r/'wx/main_window.cpp').read_text(); b=s.split('addExport("Segments')[1].split('addExport(')[0]; assert 'onExportToStructure(e)' in b and 'schematic' not in b
 assert 'name.Replace("_", " ")' in s and 'engineOutput' in s
 print('Source checks passed: NBT segment routing, 16 carpets including orange, space names')
if a.exe:
 with tempfile.TemporaryDirectory() as d:
  d=pathlib.Path(d); img=d/'orange.png'; out=d/'export'; out.mkdir()
  def chunk(t,x): return struct.pack('>I',len(x))+t+x+struct.pack('>I',zlib.crc32(t+x)&0xffffffff)
  img.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',256,128,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+bytes([216,127,51])*256)*128))+chunk(b'IEND',b''))
  conf=d/'carpets.conf'; conf.write_text('MODE(WHITELIST)\nADD(COLOR_ORANGE,orange_carpet)\n')
  subprocess.run([str(pathlib.Path(a.exe).resolve()),'--build',str(img),'--format','structure','--output',str(out),'--build-method','flat','--dithering','none','--color-method','euclidean','--color-set',str(conf),'--yes','1'],check=True)
  files=list(out.glob('*.nbt')); assert len(files)==2,files
  for f in files:
   assert '_' not in f.name,f
   data=zlib.decompress(f.read_bytes(),31)
   assert b'orange_carpet' in data and b'palette' in data and b'blocks' in data and b'size' in data
   assert b'orange_wool' not in data
  print('Compiled CLI passed: two real compressed structure NBT files, orange_carpet palette, space filenames')
