#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar um instalador avançado com Inno Setup
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def criar_script_inno_setup():
    """Criar script do Inno Setup para instalador avançado"""
    
    print("🔧 Criando Script do Inno Setup")
    print("=" * 40)
    
    # Script do Inno Setup
    inno_script = f"""; Script gerado automaticamente para Processador de DARMs
; Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

#define MyAppName "Processador de DARMs"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Sistema de Processamento Municipal"
#define MyAppExeName "Processador-DARM.exe"

[Setup]
; Informações do aplicativo
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppVerName={{#MyAppName}} {{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
OutputDir=Instalador
OutputBaseFilename=Processador-DARM-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

; Informações da interface
WizardImageFile=wizard.bmp
WizardSmallImageFile=wizard-small.bmp
SetupIconFile=icon.ico

; Configurações de instalação
DisableProgramGroupPage=yes
DisableReadyPage=no
DisableFinishedPage=no
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=yes

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
; Executável principal
Source: "dist\\Processador-DARM.exe"; DestDir: "{{app}}"; Flags: ignoreversion
; Documentação
Source: "Instalador\\README.txt"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "Instalador\\EXEMPLO.txt"; DestDir: "{{app}}"; Flags: ignoreversion
; Scripts de instalação
Source: "Instalador\\INSTALAR.bat"; DestDir: "{{app}}"; Flags: ignoreversion
; Estrutura de pastas
Source: "Instalador\\darms\\*"; DestDir: "{{app}}\\darms"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Instalador\\inserts\\*"; DestDir: "{{app}}\\inserts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Ícone no menu Iniciar
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
; Ícone na área de trabalho
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
; Ícone na barra de tarefas
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
; Executar após instalação
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
; Abrir pasta de DARMs
Filename: "{{app}}\\darms"; Description: "Abrir pasta de DARMs"; Flags: postinstall skipifsilent shellexec

[UninstallDelete]
; Remover arquivos gerados pelo usuário
Type: filesandordirs; Name: "{{app}}\\inserts\\*"
Type: filesandordirs; Name: "{{app}}\\darms\\*"

[Code]
// Código personalizado do instalador
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Criar atalho na área de trabalho se solicitado
    if IsTaskSelected('desktopicon') then
    begin
      // Código para criar atalho personalizado
    end;
  end;
end;

// Verificar se o sistema tem os requisitos mínimos
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Verificar se é Windows 10 ou superior
  if not IsWin64 then
  begin
    MsgBox('Este aplicativo requer Windows 10 ou superior (64-bit).', mbError, MB_OK);
    Result := False;
  end;
end;

// Página personalizada de boas-vindas
procedure CreateWelcomePage;
var
  WelcomePage: TWizardPage;
  WelcomeLabel: TLabel;
begin
  WelcomePage := CreateCustomPage(wpWelcome, 'Bem-vindo ao Processador de DARMs', 
    'Este assistente irá instalar o Processador de DARMs em seu computador.');
    
  WelcomeLabel := TLabel.Create(WelcomePage);
  WelcomeLabel.Parent := WelcomePage.Surface;
  WelcomeLabel.Caption := 'O Processador de DARMs é uma ferramenta automatizada para processamento de Documentos de Arrecadação de Receitas Municipais.' + #13#10 + #13#10 +
    'Funcionalidades:' + #13#10 +
    '• Extração automática de dados de PDFs' + #13#10 +
    '• Suporte a OCR para PDFs com imagens' + #13#10 +
    '• Geração de SQL compatível com Control-M' + #13#10 +
    '• Correção automática de inscrições municipais' + #13#10 +
    '• Relatórios detalhados do processamento';
  WelcomeLabel.Left := 0;
  WelcomeLabel.Top := 0;
  WelcomeLabel.Width := WelcomePage.SurfaceWidth;
  WelcomeLabel.Height := WelcomePage.SurfaceHeight;
  WelcomeLabel.AutoSize := False;
  WelcomeLabel.WordWrap := True;
end;

// Inicializar páginas personalizadas
procedure InitializeWizard();
begin
  CreateWelcomePage;
end;
"""
    
    # Salvar script do Inno Setup
    with open("Processador-DARM.iss", "w", encoding="utf-8") as f:
        f.write(inno_script)
    
    print("✅ Script do Inno Setup criado: Processador-DARM.iss")
    print("\n📋 Para compilar o instalador:")
    print("   1. Instale o Inno Setup: https://jrsoftware.org/isinfo.php")
    print("   2. Abra o arquivo Processador-DARM.iss")
    print("   3. Clique em 'Build' > 'Compile'")
    print("   4. O instalador será gerado na pasta Instalador/")
    
    return "Processador-DARM.iss"

def criar_instalador_portable():
    """Criar versão portável do instalador"""
    
    print("\n📦 Criando Versão Portável")
    print("=" * 30)
    
    portable_dir = Path("Instalador-Portavel")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # Copiar executável
    shutil.copy2("dist/Processador-DARM.exe", portable_dir / "Processador-DARM.exe")
    
    # Criar pastas
    (portable_dir / "darms").mkdir()
    (portable_dir / "inserts").mkdir()
    
    # Criar launcher personalizado
    launcher_content = """@echo off
title Processador de DARMs v1.0.0
color 0A

echo.
echo ========================================
echo    PROCESSADOR DE DARMs v1.0.0
echo ========================================
echo.
echo Iniciando processamento...
echo.

REM Executar o processador
Processador-DARM.exe

echo.
echo Processamento concluido!
echo Verifique a pasta 'inserts' para os resultados.
echo.
pause
"""
    
    with open(portable_dir / "EXECUTAR.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Copiar documentação
    shutil.copy2("Instalador/README.txt", portable_dir / "README.txt")
    shutil.copy2("Instalador/EXEMPLO.txt", portable_dir / "EXEMPLO.txt")
    
    print("✅ Versão portável criada em: Instalador-Portavel/")
    print("📁 Conteúdo:")
    for item in portable_dir.rglob("*"):
        if item.is_file():
            print(f"   - {item.name}")
    
    return portable_dir

if __name__ == "__main__":
    # Criar script do Inno Setup
    inno_file = criar_script_inno_setup()
    
    # Criar versão portável
    portable_dir = criar_instalador_portable()
    
    print(f"\n🎯 Instaladores criados:")
    print(f"   1. Script Inno Setup: {inno_file}")
    print(f"   2. Versão Portável: {portable_dir}")
    print(f"   3. Instalador ZIP: Processador-DARM-Instalador-*.zip")

