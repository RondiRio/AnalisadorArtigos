; Script do Inno Setup para Analisador de Artigos
; Versão: 1.0.0
; Autor: Seu Nome

[Setup]
; Informações básicas da aplicação
AppName=Analisador de Artigos e Livros
AppVersion=1.0.0
AppVerName=Analisador de Artigos e Livros 1.0.0
AppPublisher=Analisador de Artigos
AppPublisherURL=https://github.com/seuusuario/analisador-artigos
AppSupportURL=https://github.com/seuusuario/analisador-artigos/issues
AppUpdatesURL=https://github.com/seuusuario/analisador-artigos/releases

; Configurações de instalação
DefaultDirName={autopf}\Analisador de Artigos
DefaultGroupName=Analisador de Artigos
AllowNoIcons=yes
LicenseFile=license.txt
InfoBeforeFile=README.md
OutputDir=installer_output
OutputBaseFilename=AnalisadorArtigos_Setup_v1.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; Configurações de segurança e compatibilidade
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Configurações visuais
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associatefiles"; Description: "Associar arquivos .csv com o Analisador"; GroupDescription: "Associações de arquivo:"

[Files]
; Arquivo principal
Source: "dist\AnalisadorArtigos.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos de documentação
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

; Arquivo de exemplo (opcional)
Source: "exemplo.csv"; DestDir: "{app}\exemplos"; Flags: ignoreversion; Check: FileExists('exemplo.csv')

[Registry]
; Associação de arquivos CSV (opcional)
Root: HKA; Subkey: "Software\Classes\.csv\OpenWithProgids"; ValueType: string; ValueName: "AnalisadorArtigos.csv"; ValueData: ""; Flags: uninsdeletevalue; Tasks: associatefiles
Root: HKA; Subkey: "Software\Classes\AnalisadorArtigos.csv"; ValueType: string; ValueName: ""; ValueData: "Arquivo CSV para Analisador de Artigos"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKA; Subkey: "Software\Classes\AnalisadorArtigos.csv\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\AnalisadorArtigos.exe,0"; Tasks: associatefiles
Root: HKA; Subkey: "Software\Classes\AnalisadorArtigos.csv\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\AnalisadorArtigos.exe"" ""%1"""; Tasks: associatefiles

[Icons]
; Menu Iniciar
Name: "{group}\Analisador de Artigos"; Filename: "{app}\AnalisadorArtigos.exe"; Comment: "Analisar listas de artigos e livros"
Name: "{group}\Leia-me"; Filename: "{app}\README.md"; Comment: "Instruções de uso"
Name: "{group}\{cm:UninstallProgram,Analisador de Artigos}"; Filename: "{uninstallexe}"

; Área de trabalho
Name: "{autodesktop}\Analisador de Artigos"; Filename: "{app}\AnalisadorArtigos.exe"; Tasks: desktopicon; Comment: "Analisar listas de artigos e livros"

; Barra de tarefas (Windows 7 e anterior)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Analisador de Artigos"; Filename: "{app}\AnalisadorArtigos.exe"; Tasks: quicklaunchicon

[Run]
; Executar após instalação
Filename: "{app}\AnalisadorArtigos.exe"; Description: "{cm:LaunchProgram,Analisador de Artigos}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpar arquivos criados pelo usuário (opcional)
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\temp"

[Code]
// Funções em Pascal Script para customizações

function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function InitializeSetup(): Boolean;
var
  V: Integer;
  iResultCode: Integer;
  sUnInstallString: string;
begin
  Result := True; // Permite continuar com a instalação por padrão
  
  // Verifica se há uma versão anterior instalada
  if RegValueExists(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\Analisador de Artigos_is1', 'UninstallString') then
  begin
    V := MsgBox(ExpandConstant('Uma versão anterior do {#SetupSetting("AppName")} foi detectada.' + #13#13 +
                'É recomendado desinstalar a versão anterior antes de continuar.' + #13#13 +
                'Deseja desinstalar agora?'), mbInformation, MB_YESNO);
    if V = IDYES then
    begin
      sUnInstallString := GetUninstallString();
      sUnInstallString := RemoveQuotes(sUnInstallString);
      if Exec(sUnInstallString, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
        Result := True
      else
      begin
        Result := False;
        MsgBox('Falha ao desinstalar a versão anterior. Instalação cancelada.', mbError, MB_OK);
      end;
    end
    else
      Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Aqui você pode adicionar ações pós-instalação
    // Por exemplo, criar arquivos de configuração, registrar no Windows, etc.
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // Pular página de seleção de componentes se não houver componentes
  if PageID = wpSelectComponents then
    Result := True
  else
    Result := False;
end;

// Verificar se um arquivo existe
function FileExists(const FileName: string): Boolean;
begin
  Result := FileExists(ExpandConstant('{src}\' + FileName));
end;