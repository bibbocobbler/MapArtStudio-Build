from pathlib import Path
import sys
root=Path(sys.argv[1])/'src'
def edit(file, old, new, count=1):
 p=root/file; s=p.read_text(encoding='utf-8-sig'); assert s.count(old)==count,(file,old,s.count(old)); p.write_text(s.replace(old,new),encoding='utf-8')
carpets='MODE(WHITELIST)\\n'+''.join('ADD('+c+','+b+'_carpet)\\n' for c,b in [('SNOW','white'),('COLOR_ORANGE','orange'),('COLOR_MAGENTA','magenta'),('COLOR_LIGHT_BLUE','light_blue'),('COLOR_YELLOW','yellow'),('COLOR_LIGHT_GREEN','lime'),('COLOR_PINK','pink'),('COLOR_GRAY','gray'),('COLOR_LIGHT_GRAY','light_gray'),('COLOR_CYAN','cyan'),('COLOR_PURPLE','purple'),('COLOR_BLUE','blue'),('COLOR_BROWN','brown'),('COLOR_GREEN','green'),('COLOR_RED','red'),('COLOR_BLACK','black')])
# Python literal escaping: C++ needs backslash-n, not double backslashes.
carpets=carpets.replace('\\\\n','\\n')
edit('mapart/project.cpp','colorSetConf = "MODE(BLACKLIST)\\n";', 'colorSetConf = "'+carpets+'";')
for file in ['wx/materials_window.cpp','wx/main_window.cpp']:
 edit(file,'ADD(SNOW,white_carpet)\\n','ADD(SNOW,white_carpet)\\nADD(COLOR_ORANGE,orange_carpet)\\n')
remember='    { const std::string saved = tools::getRememberedValue("studio-materials-v1.conf");\n      if (!saved.empty()) project.colorSetConf = saved; }\n'
edit('wx/main_window.cpp',remember,'',2)
edit('wx/main_window.cpp','if (carpetMode) { exportCarpetUsingOriginal("schematic-segmented"); return; }\n        onExportToSchematicZip(e);','onExportToStructure(e);')
edit('wx/main_window.cpp','Segments (folder, 128 x 129)...','Segments (.nbt folder, 128 x 129)...')
for file in ['wx/worker_thread.cpp','main_console.cpp']:
 p=root/file; s=p.read_text(encoding='utf-8-sig')
 # Keep vanilla map_#.dat names: Minecraft requires them before 26.1.
 for a,b in [('"map_" << (total + 1)','"map " << (total + 1)'),('"_base.nbt"','" base.nbt"'),('"_base.schem"','" base.schem"'),('"bases/map_"','"bases/map "')]: s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
edit('wx/main_window.cpp','#include <wx/filename.h>','#include <wx/filename.h>\n#include <wx/dir.h>')
# Export legacy segments to an isolated directory, then publish only these new files.
edit('wx/main_window.cpp','    const wxString bm = (carpetMode==2)', '''    const wxString exportDir = tmp + "-segments";
    const bool segments = format == "structure" || format == "schematic-segmented";
    if (segments && !wxFileName::Mkdir(exportDir)) {
        wxMessageBox("Cannot create temporary export folder.", "Export error", wxOK | wxICON_ERROR);
        wxRemoveFile(png); wxRemoveFile(conf); wxRemoveFile(tmp); return true;
    }
    const wxString engineOutput = segments ? exportDir : output;
    const wxString bm = (carpetMode==2)''')
edit('wx/main_window.cpp','+output+"\\\" --build-method "+bm+', '+engineOutput+"\\\" --build-method "+bm+')
edit('wx/main_window.cpp','    const long code=wxExecute(command,wxEXEC_SYNC);','''    long code=wxExecute(command,wxEXEC_SYNC);
    if (segments && code == 0) {
        wxArrayString files;
        wxDir::GetAllFiles(exportDir, &files);
        if (files.empty()) code = -1;
        for (const auto &file : files) {
            wxString name = wxFileName(file).GetFullName();
            name.Replace("_", " ");
            const wxString destination = wxFileName(output, name).GetFullPath();
            if (!wxCopyFile(file, destination, false)) { code = -1; break; }
        }
        if (code == 0) wxFileName::Rmdir(exportDir, wxPATH_RMDIR_RECURSIVE);
    }
    if (segments && code != 0)
        wxMessageBox("Export failed or a destination file already exists. Temporary files retained at: " + exportDir,
            "Export error", wxOK | wxICON_ERROR);''')
print('NBT segments, space-separated structure names, 16-colour carpet defaults installed')

edit('wx/main_window.cpp', '''    StructureExportDialog dialog(project.version, ExportDialogMode::Structure);
    if (dialog.ShowModal() == wxID_CANCEL)
    {
        return; // the user changed idea...
    }

    this->workerThread->requestExportStruct(project, dialog.getPath());''', '''    wxDirDialog dialog(this, "Choose output folder for NBT segments", wxEmptyString,
        wxDD_DEFAULT_STYLE | wxDD_DIR_MUST_EXIST);
    if (dialog.ShowModal() == wxID_CANCEL) return;
    this->workerThread->requestExportStruct(project, dialog.GetPath().ToStdString());''')

edit('wx/main_window.cpp', ' --yes 1', ' --yes')

edit('wx/materials_window.cpp', '    menuBar->Append(menuPresets, "&Presets");', '    menuPresets->Check(ID_Preset_carpets, true);\n    menuBar->Append(menuPresets, "&Presets");')

# The console image handlers require a wxWidgets runtime as well as handler registration.
edit('main_console.cpp', '#include "version.h"', '#include "version.h"\n#include <wx/init.h>')
edit('main_console.cpp', 'int main(int argc, char **argv)\n{', 'int main(int argc, char **argv)\n{\n    wxInitializer wxRuntime;\n    if (!wxRuntime.IsOk()) { std::cerr << "Cannot initialize image runtime" << std::endl; return 1; }')

# Function resource names, like legacy map data names, must remain valid Minecraft identifiers.
for file in ['wx/worker_thread.cpp', 'main_console.cpp']:
 edit(file, 'ss2 << "map " << (total + 1) << ".mcfunction";', 'ss2 << "map_" << (total + 1) << ".mcfunction";')
