# Rebuilds every revision pack from src\*.tex and copies the PDFs next to this script.
# Run:  powershell -ExecutionPolicy Bypass -File build.ps1
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$src = Join-Path $root 'src'
Push-Location $src
foreach ($tex in Get-ChildItem -Filter '0*.tex' | Sort-Object Name) {
    Write-Host "Building $($tex.BaseName)..."
    1..2 | ForEach-Object { pdflatex -interaction=nonstopmode $tex.Name | Out-Null }
    if (Select-String -Path "$($tex.BaseName).log" -Pattern '^!' -Quiet) {
        Write-Host "  ERRORS - see src\$($tex.BaseName).log" -ForegroundColor Red
    }
    Copy-Item "$($tex.BaseName).pdf" $root -Force
}
Pop-Location
Write-Host "Done. PDFs are in $root"
