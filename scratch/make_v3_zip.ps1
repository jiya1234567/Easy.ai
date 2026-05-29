$src = 'c:\Universal_Lab_AP_Phillips'
$dst = 'c:\Universal_Lab_AP_Phillips\Universal_Lab_Cloud_V3.zip'

# Remove old zip
if (Test-Path $dst) { Remove-Item $dst -Force }

Add-Type -Assembly 'System.IO.Compression.FileSystem'
$zip = [System.IO.Compression.ZipFile]::Open($dst, 'Create')

$excludePatterns = @('\.git', '__pycache__', 'node_modules', 'bore_bin', '\.vscode', '\.zip$')

Get-ChildItem -Path $src -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($src.Length + 1)
    $skip = $false
    foreach ($pat in $excludePatterns) {
        if ($rel -match $pat) { $skip = $true; break }
    }
    if (-not $skip) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $zip, $_.FullName, $rel, 'Optimal'
        ) | Out-Null
        Write-Host "  + $rel"
    }
}

$zip.Dispose()

$size = [math]::Round((Get-Item $dst).Length / 1MB, 2)
Write-Host ""
Write-Host "====================================="
Write-Host "  ZIP CREATED: Universal_Lab_Cloud_V3.zip"
Write-Host "  Size: $size MB"
Write-Host "  Path: $dst"
Write-Host "====================================="
