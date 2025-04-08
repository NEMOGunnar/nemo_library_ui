[Setup]
AppName=Nemo Library
AppVersion=1.0
DefaultDirName={commonpf}\NemoLibrary
DefaultGroupName=Nemo Library
OutputBaseFilename=NemoLibrarySetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\NemoLibraryUI.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Nemo Library"; Filename: "{app}\NemoLibraryUI.exe"
Name: "{group}\Uninstall Nemo Library"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\NemoLibraryUI.exe"; Description: "Launch Nemo Library"; Flags: nowait postinstall skipifsilent
