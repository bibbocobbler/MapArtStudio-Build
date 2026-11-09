from pathlib import Path
import sys
p = Path(sys.argv[1]) / 'src/wx/main_window.cpp'
s = p.read_text(encoding='utf-8-sig')
def edit(old,new):
    global s
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new,1)
helper = '''namespace {
bool chooseNewSegmentFolder(wxWindow *parent, wxString &output)
{
    wxFileDialog dialog(parent, "Export NBT segments - enter a new folder name",
        wxEmptyString, "mapart", "Folder name|*", wxFD_SAVE);
    if (dialog.ShowModal() != wxID_OK) return false;
    const wxString path = dialog.GetPath();
    if (wxDirExists(path) || wxFileExists(path)) {
        wxMessageBox("That name already exists. Choose a new folder name.",
            "Choose a new folder", wxOK | wxICON_INFORMATION, parent);
        return false;
    }
    if (!wxFileName::Mkdir(path, wxS_DIR_DEFAULT, wxPATH_MKDIR_FULL)) {
        wxMessageBox("The export folder could not be created. Choose a writable destination.",
            "Export error", wxOK | wxICON_ERROR, parent);
        return false;
    }
    output = path;
    return true;
}
}

'''
edit('using namespace std;',helper+'using namespace std;')
edit('''    wxDirDialog dialog(this, "Choose output folder for NBT segments", wxEmptyString,
        wxDD_DEFAULT_STYLE | wxDD_DIR_MUST_EXIST);
    if (dialog.ShowModal() == wxID_CANCEL) return;
    this->workerThread->requestExportStruct(project, dialog.GetPath().ToStdString());''', '''    wxString output;
    if (!chooseNewSegmentFolder(this, output)) return;
    this->workerThread->requestExportStruct(project, output.ToStdString());''')
edit('''    if (format == "schematic-segmented" || format == "schematic" || format == "structure") {''', '''    if (format == "structure") {
        if (!chooseNewSegmentFolder(this, output)) return true;
    } else if (format == "schematic-segmented" || format == "schematic") {''')
p.write_text(s,encoding='utf-8')
print('Native and legacy NBT Segments export now creates the named folder automatically')
