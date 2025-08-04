$folder = Get-Location
Write-Host "Watching for changes in $folder"

while ($true) {
    Get-ChildItem -Recurse -Include *.py,*.html,*.css,*.js | 
        Where-Object { $_.LastWriteTime -gt (Get-Date).AddSeconds(-5) } |
        ForEach-Object {
            git add .
            git commit -m "Auto commit at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git push
            Start-Sleep -Seconds 10
        }
    Start-Sleep -Seconds 3
}
