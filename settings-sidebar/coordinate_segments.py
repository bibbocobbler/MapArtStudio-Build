from pathlib import Path
import shutil, sys
root = Path(sys.argv[1]) / 'src'
here = Path(__file__).resolve().parent
shutil.copy2(here / 'segment_names.h', root / 'mapart/segment_names.h')
def edit(file, old, new, count=1):
    p = root / file
    text = p.read_text(encoding='utf-8-sig')
    assert text.count(old) == count, (file, old, text.count(old))
    p.write_text(text.replace(old, new), encoding='utf-8')
for file, header in [('wx/worker_thread.cpp','../mapart/segment_names.h'),
                     ('wx/main_window.cpp','../mapart/segment_names.h'),
                     ('main_console.cpp','mapart/segment_names.h')]:
    p = root / file
    p.write_text('#include "' + header + '"\n' + p.read_text(encoding='utf-8-sig'), encoding='utf-8')
# Only the folder structure exporter changes; ZIP and single-file exports retain their behavior.
p = root / 'wx/worker_thread.cpp'
s = p.read_text(encoding='utf-8-sig')
a = s.index('void WorkerThread::ExportStruct(')
b = s.index('\nvoid WorkerThread::', a + 10)
block = s[a:b]
assert block.count('ss2 << "map " << (total + 1) << ".nbt";') == 1
assert block.count('ss3 << "map " << (total + 1) << " base.nbt";') == 1
block = block.replace('ss2 << "map " << (total + 1) << ".nbt";', 'ss2 << mapart::segmentFileName(copyOutPath, mapZ, mapX, mapsCountZ);')
block = block.replace('ss3 << "map " << (total + 1) << " base.nbt";', 'ss3 << mapart::segmentFileName(copyOutPath, mapZ, mapX, mapsCountZ, " base.nbt");')
p.write_text(s[:a] + block + s[b:], encoding='utf-8')
edit('main_console.cpp', 'ss2 << "map " << (total + 1) << ".nbt";',
     'ss2 << mapart::segmentFileName(outputPath, mapZ, mapX, mapsCountZ);')
edit('wx/main_window.cpp', '''            name.Replace("_", " ");
            const wxString destination''', '''            name.Replace("_", " ");
            if (format == "structure") {
                const wxString stem = wxFileName(file).GetName();
                long ordinal = 0;
                const int columns = preview.GetWidth() / MAP_WIDTH;
                const int rows = preview.GetHeight() / MAP_HEIGHT;
                if (!stem.StartsWith("map_") || !stem.Mid(4).ToLong(&ordinal) ||
                    ordinal < 1 || columns <= 0 || rows <= 0 || ordinal > columns * rows ||
                    wxFileName(file).GetExt().CmpNoCase("nbt") != 0) {
                    code = -1; break;
                }
                name = wxString::FromUTF8(mapart::legacySegmentFileName(
                    output.ToStdString(), ordinal, columns, rows));
            }
            const wxString destination''')
# Compile the shared helper's regression test along with the app.
shutil.copy2(here / 'segment_names_test.cpp', root / 'segment_names_test.cpp')
p = root / 'CMakeLists.txt'
p.write_text(p.read_text() + '\nadd_executable(segment-names-test "segment_names_test.cpp")\n', encoding='utf-8')
print('Folder-name + bottom-origin row,column naming installed for native and legacy NBT segments')
