<#
.SYNOPSIS
    Download RDKit.js WASM engine for molecular coordinate generation.

.DESCRIPTION
    Downloads RDKit_minimal.js and RDKit_minimal.wasm from the official
    RDKit GitHub release. These files are required by tools/generate_coords.js
    for generating 2D molecular coordinates from SMILES strings.

    The RDKit.js WASM files are ~7MB total and are not included in the git
    repository due to size. Run this script once after cloning.

.NOTES
    Source: https://github.com/rdkit/rdkit/releases
    Version: RDKit 2024.09.5 (or latest Release_ tag)
    License: BSD-3-Clause (RDKit)
#>

param(
    [string]$OutputDir = "rdkit",
    [string]$Version = "2024.09.5"
)

$ErrorActionPreference = "Stop"

# RDKit.js release assets are hosted on GitHub
$baseUrl = "https://github.com/rdkit/rdkit/releases/download/Release_$($Version.Replace('.', '_'))"

$files = @(
    @{ Name = "RDKit_minimal.js";  Url = "$baseUrl/RDKit_minimal.js"  },
    @{ Name = "RDKit_minimal.wasm"; Url = "$baseUrl/RDKit_minimal.wasm" }
)

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "[INFO] Created directory: $OutputDir" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== RDKit.js WASM Downloader ===" -ForegroundColor Green
Write-Host "Version: $Version"
Write-Host "Output:  $OutputDir"
Write-Host "Source:  $baseUrl"
Write-Host ""

$success = 0
$failed = 0

foreach ($file in $files) {
    $outPath = Join-Path $OutputDir $file.Name

    # Skip if already exists and is non-empty
    if (Test-Path $outPath) {
        $existingSize = (Get-Item $outPath).Length
        if ($existingSize -gt 1000) {
            Write-Host "[SKIP] $($file.Name) already exists ($([math]::Round($existingSize/1KB, 1)) KB)" -ForegroundColor Yellow
            $success++
            continue
        }
    }

    Write-Host "[DOWNLOAD] $($file.Name)..." -ForegroundColor Cyan

    try {
        # Use Invoke-WebRequest with progress bar disabled for speed
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $file.Url -OutFile $outPath -UseBasicParsing -TimeoutSec 120

        $size = (Get-Item $outPath).Length
        if ($size -lt 100) {
            throw "Downloaded file too small ($size bytes) — likely an error page"
        }

        Write-Host "[OK] $($file.Name) downloaded ($([math]::Round($size/1KB, 1)) KB)" -ForegroundColor Green
        $success++
    }
    catch {
        Write-Host "[FAIL] $($file.Name): $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "       Try downloading manually from: $($file.Url)" -ForegroundColor DarkGray
        $failed++

        # Remove partial file
        if (Test-Path $outPath) {
            Remove-Item $outPath -Force -ErrorAction SilentlyContinue
        }
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Green
Write-Host "Success: $success / $($files.Count)"
if ($failed -gt 0) {
    Write-Host "Failed:  $failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual download instructions:" -ForegroundColor Yellow
    Write-Host "  1. Visit: https://github.com/rdkit/rdkit/releases"
    Write-Host "  2. Find the latest Release_ tag (e.g., Release_2024_09_5)"
    Write-Host "  3. Download RDKit_minimal.js and RDKit_minimal.wasm"
    Write-Host "  4. Place them in the '$OutputDir/' directory"
    exit 1
}

Write-Host ""
Write-Host "[DONE] RDKit.js WASM engine ready. You can now run:" -ForegroundColor Green
Write-Host "       node tools/generate_coords.js --smiles 'c1ccccc1' --name benzene" -ForegroundColor Cyan
Write-Host ""
