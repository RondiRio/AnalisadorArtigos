[Setup]
AppName=Analisador de Artigos e Livros
AppVersion=2.0.0
AppPublisher=Analisador de Artigos
DefaultDirName={autopf}\Analisador de Artigos
DefaultGroupName=Analisador de Artigos
OutputDir=installer
OutputBaseFilename=AnalisadorArtigos_Setup_v2.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na área de trabalho"; GroupDescription: "Ícones adicionais:"; Flags: unchecked

[Files]
Source: "dist\AnalisadorArtigos.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Analisador de Artigos"; Filename: "{app}\AnalisadorArtigos.exe"
Name: "{autodesktop}\Analisador de Artigos"; Filename: "{app}\AnalisadorArtigos.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AnalisadorArtigos.exe"; Description: "Executar Analisador de Artigos"; Flags: nowait postinstall skipifsilent
