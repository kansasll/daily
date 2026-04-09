[Setup]
AppId={{A7E8D94A-4A26-42EA-8A60-2E799D50A663}
AppName=Daily Scheduler
AppVersion=1.1.0
AppPublisher=Daily Scheduler Team
DefaultDirName={localappdata}\Programs\Daily Scheduler
DefaultGroupName=Daily Scheduler
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=DailyScheduler-Setup-1.1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\DailyScheduler.exe

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional options:"

[Files]
Source: "..\dist\DailyScheduler.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Daily Scheduler"; Filename: "{app}\DailyScheduler.exe"
Name: "{autodesktop}\Daily Scheduler"; Filename: "{app}\DailyScheduler.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\DailyScheduler.exe"; Description: "Launch Daily Scheduler now"; Flags: nowait postinstall skipifsilent
