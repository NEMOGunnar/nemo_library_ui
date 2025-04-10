[Setup]
AppName=Nemo Library
AppVersion=1.0
DefaultDirName={commonpf}\NemoLibrary
DefaultGroupName=Nemo Library
OutputBaseFilename=NemoUISetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\NemoUI.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Nemo Library"; Filename: "{app}\NemoUI.exe"
Name: "{group}\Uninstall Nemo Library"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\NemoUI.exe"; Description: "Launch Nemo Library"; Flags: nowait postinstall skipifsilent
