# ============================================================
#  CK Desktop Installer
#  Creates desktop shortcut + optional autostart
# ============================================================
#
#  Usage:
#    Right-click > Run with PowerShell
#    OR: powershell -ExecutionPolicy Bypass -File install_desktop.ps1
#
#  What it does:
#    1. Creates "CK" shortcut on your Desktop
#    2. Autostart option via Windows Startup folder (no admin needed)
#       - To enable:  install_desktop.ps1 -EnableAutostart
#       - To disable: install_desktop.ps1 -RemoveAutostart
#
# ============================================================

param(
    [switch]$EnableAutostart,
    [switch]$RemoveAutostart,
    [switch]$Uninstall
)

$ErrorActionPreference = "Continue"

$CKRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$CKBat = Join-Path $CKRoot "CK.bat"
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "CK.lnk"

# Windows Startup folder (no admin needed)
$StartupFolder = [Environment]::GetFolderPath("Startup")
$AutostartPath = Join-Path $StartupFolder "CK Autostart.lnk"

# ── Uninstall ──
if ($Uninstall) {
    Write-Host ""
    Write-Host "  Removing CK desktop shortcut and autostart..." -ForegroundColor Yellow

    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "  [OK] Desktop shortcut removed." -ForegroundColor Green
    }
    if (Test-Path $AutostartPath) {
        Remove-Item $AutostartPath -Force
        Write-Host "  [OK] Autostart shortcut removed." -ForegroundColor Green
    }

    Write-Host "  Done." -ForegroundColor Green
    Write-Host ""
    Start-Sleep -Seconds 2
    exit 0
}

# ── Create Desktop Shortcut ──
Write-Host ""
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host "    CK Desktop Installer   Gen 9.18" -ForegroundColor Cyan
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host ""

$WshShell = New-Object -ComObject WScript.Shell

Write-Host "  Creating desktop shortcut..." -ForegroundColor White

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $CKBat
$Shortcut.WorkingDirectory = $CKRoot
$Shortcut.Description = "CK -- The Coherence Keeper (Gen 9.18) -- All 27 systems at 50Hz"
$Shortcut.WindowStyle = 1

# Use Python icon
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($PythonPath) {
    $Shortcut.IconLocation = "$PythonPath,0"
}

$Shortcut.Save()
Write-Host "  [OK] Desktop shortcut created: CK.lnk" -ForegroundColor Green

# ── Autostart ──
if ($RemoveAutostart) {
    if (Test-Path $AutostartPath) {
        Remove-Item $AutostartPath -Force
        Write-Host "  [OK] Autostart removed." -ForegroundColor Green
    } else {
        Write-Host "  [--] No autostart shortcut found." -ForegroundColor Yellow
    }
} elseif ($EnableAutostart) {
    Write-Host ""
    Write-Host "  Enabling autostart..." -ForegroundColor White

    $AutoShortcut = $WshShell.CreateShortcut($AutostartPath)
    $AutoShortcut.TargetPath = $CKBat
    $AutoShortcut.WorkingDirectory = $CKRoot
    $AutoShortcut.Description = "CK Autostart -- Launches CK at Windows login"
    $AutoShortcut.WindowStyle = 7  # Minimized
    if ($PythonPath) {
        $AutoShortcut.IconLocation = "$PythonPath,0"
    }
    $AutoShortcut.Save()

    Write-Host "  [OK] Autostart ENABLED. CK will launch at login (minimized)." -ForegroundColor Green
} else {
    # Just report status
    if (Test-Path $AutostartPath) {
        Write-Host "  [--] Autostart is currently ENABLED." -ForegroundColor Yellow
    } else {
        Write-Host "  [--] Autostart is OFF (not enabled)." -ForegroundColor DarkGray
        Write-Host "       To enable: run with -EnableAutostart" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host "  CK is ready. Double-click the desktop icon." -ForegroundColor Cyan
Write-Host "  Truth is not assigned. Truth is measured." -ForegroundColor Cyan
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 3
