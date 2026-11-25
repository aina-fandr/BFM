$root = 'C:\Users\Nek''s\Documents\Nekena\PROJET\STAGE_L3\PROJET BANQUE CENTRALE'
$output = Join-Path $root 'STRUCTURE_COMPLETE.md'
$excludedNames = @('.git', 'node_modules', 'dist', '.vite', '__pycache__')

$directories = New-Object System.Collections.Generic.List[System.IO.DirectoryInfo]
$files = New-Object System.Collections.Generic.List[System.IO.FileInfo]

foreach ($item in Get-ChildItem -LiteralPath $root -Recurse -Force) {
    $relative = $item.FullName.Substring($root.Length)
    $skip = $false
    foreach ($name in $excludedNames) {
        if ($relative -like ('*\' + $name + '\*') -or $relative -like ('*\' + $name)) {
            $skip = $true
            break
        }
    }
    if (-not $skip) {
        if ($item.PSIsContainer) {
            $directories.Add($item)
        } else {
            $files.Add($item)
        }
    }
}

$directories = @($directories | Sort-Object FullName)
$files = @($files | Sort-Object FullName)
$lines = New-Object System.Collections.Generic.List[string]

$lines.Add('# Structure complete - Projet Banque Centrale')
$lines.Add('')
$lines.Add('**Racine :** C:\Users\Nek''s\Documents\Nekena\PROJET\STAGE_L3\PROJET BANQUE CENTRALE')
$lines.Add('')
$lines.Add('**Date :** 23 novembre 2026')
$lines.Add('')
$lines.Add('Ce document inventorie tous les dossiers et fichiers presents dans le perimetre actif du projet.')
$lines.Add('')
$lines.Add('## Statistiques')
$lines.Add('')
$lines.Add('- ' + $directories.Count + ' dossiers')
$lines.Add('- ' + $files.Count + ' fichiers inventories')
$lines.Add('')
$lines.Add('## Structure complete des dossiers')
$lines.Add('')
$lines.Add('```text')
$lines.Add('PROJET BANQUE CENTRALE/')

foreach ($directory in $directories) {
    $relative = $directory.FullName.Substring($root.Length).TrimStart('\')
    $depth = ($relative.Split('\', [System.StringSplitOptions]::RemoveEmptyEntries)).Count
    $lines.Add(('    ' * $depth) + $directory.Name + '/')
}

$lines.Add('```')
$lines.Add('')
$lines.Add('## Liste complete des fichiers')
$lines.Add('')
$lines.Add('| Fichier | Taille |')
$lines.Add('|---|---:|')

foreach ($file in $files) {
    $relative = $file.FullName.Substring($root.Length).TrimStart('\').Replace('\', '/')
    $sizeKb = [Math]::Max(1, [Math]::Round($file.Length / 1KB, 1))
    $lines.Add('| `' + $relative + '` | ' + $sizeKb + ' Ko |')
}

[System.IO.File]::WriteAllLines($output, $lines, [System.Text.UTF8Encoding]::new($false))
Write-Output $output
