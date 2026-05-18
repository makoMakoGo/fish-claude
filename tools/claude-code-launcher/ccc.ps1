# ccc - Interactive Claude Code launcher with settings picker
# Lists settings* files in the current user's Claude config directory,
# then launches claude with --dangerously-skip-permissions using the selected file.
#
# Usage:  . tools/ccc.ps1     (dot-source to get the function into your session)
#         ccc                  (then follow the prompts)

function ccc {
    $claudeDir = "$env:USERPROFILE\.claude"

    if (Test-Path $claudeDir) {
        $settingsFiles = Get-ChildItem -Path $claudeDir -Filter "settings*" -File

        if ($settingsFiles.Count -eq 0) {
            Write-Output "No settings files found."
            return
        }

        Write-Output "Select a settings file:"
        for ($i = 0; $i -lt $settingsFiles.Count; $i++) {
            Write-Output "$($i + 1). $($settingsFiles[$i].Name)"
        }

        $choice = Read-Host "Choice"

        if ($choice -match '^\d+$' -and [int]$choice -ge 1 -and [int]$choice -le $settingsFiles.Count) {
            $selected = $settingsFiles[[int]$choice - 1]
            Write-Output "Running: claude --dangerously-skip-permissions --settings $claudeDir\$($selected.Name)"
            & claude --dangerously-skip-permissions --settings "$claudeDir\$($selected.Name)"
        }
        else {
            Write-Output "Invalid choice."
        }
    }
    else {
        Write-Output "$claudeDir does not exist."
    }
}
