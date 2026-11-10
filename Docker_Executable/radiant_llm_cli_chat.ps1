# RADIANT-LLM -- all-in-one: starts the container if it isn't already running
# (same as .\start.ps1, auto-detecting GPU), waits for it to be healthy, then
# drops straight into a terminal chat loop against it.
#
# Usage: .\radiant_llm_cli_chat.ps1
#
# This does NOT stop the container when you exit the chat (type "exit"/
# "quit"/Ctrl+C) -- it keeps running in the background afterward, same as
# if you'd started it with .\start.ps1. Stop it yourself whenever you're done:
#   docker compose down
#
# In the chat: "/model <name>" switches models, "/typewriter" toggles the
# typing animation. Set $env:RADIANT_LLM_TYPEWRITER = "0" before launching
# to start with it off.

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$Port = 8060
$Base = "http://localhost:$Port"
$Typewriter = if ($env:RADIANT_LLM_TYPEWRITER) { $env:RADIANT_LLM_TYPEWRITER } else { "1" }

$SpinFrames = @("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
$HrLine = "────────────────────────────────────────────────────────"
$ThinkElapsed = 0

function Write-Hr {
    Write-Host $HrLine -ForegroundColor DarkGray
}

function Set-CursorVisible {
    # [Console]::CursorVisible throws "The handle is invalid" when stdout is
    # redirected or there's no real console (e.g. piped/non-interactive runs)
    # -- swallow that the same way the bash version no-ops tput when it can't
    # control the terminal.
    param([bool]$Visible)
    try { [Console]::CursorVisible = $Visible } catch { }
}

function Clear-Line {
    Write-Host -NoNewline ("`r" + (" " * 100) + "`r")
}

function Test-Healthy {
    try {
        Invoke-RestMethod -Uri "$Base/health" -TimeoutSec 3 -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Invoke-ApiWithSpinner {
    # Runs a POST (or GET) against the API in the background while drawing a
    # spinner with elapsed time. Returns the parsed JSON response, or $null
    # with $Script:ApiError set if the call failed outright (not a JSON error
    # body -- those are returned normally for the caller to inspect).
    param(
        [Parameter(Mandatory)] [string]$Uri,
        [string]$Method = "Get",
        [hashtable]$BodyObject,
        [Parameter(Mandatory)] [string]$Message,
        [int]$TimeoutSec = 60
    )

    $bodyJson = if ($BodyObject) { $BodyObject | ConvertTo-Json -Compress } else { $null }

    $job = Start-Job -ScriptBlock {
        param($uri, $method, $bodyJson, $timeout)
        try {
            if ($bodyJson) {
                Invoke-RestMethod -Uri $uri -Method $method -ContentType "application/json" -Body $bodyJson -TimeoutSec $timeout
            } else {
                Invoke-RestMethod -Uri $uri -Method $method -TimeoutSec $timeout
            }
        } catch {
            if ($_.ErrorDetails.Message) {
                # Server returned a JSON error body (e.g. 4xx/5xx) -- pass it
                # through as-is so the caller can parse .detail/.error from it.
                $_.ErrorDetails.Message | ConvertFrom-Json
            } else {
                [pscustomobject]@{ error = $_.Exception.Message }
            }
        }
    } -ArgumentList $Uri, $Method, $bodyJson, $TimeoutSec

    $start = Get-Date
    $i = 0
    Set-CursorVisible $false
    try {
        while ($job.State -eq "Running") {
            $elapsed = [int]((Get-Date) - $start).TotalSeconds
            Write-Host -NoNewline "`r"
            Write-Host -NoNewline -ForegroundColor Yellow $SpinFrames[$i]
            Write-Host -NoNewline " $Message... "
            Write-Host -NoNewline -ForegroundColor DarkGray "(${elapsed}s)"
            $i = ($i + 1) % $SpinFrames.Count
            Start-Sleep -Milliseconds 100
        }
    } finally {
        Clear-Line
        Set-CursorVisible $true
    }
    $Script:ThinkElapsed = [int]((Get-Date) - $start).TotalSeconds
    $result = Receive-Job -Job $job
    Remove-Job -Job $job -Force
    return $result
}

function Write-Typewriter {
    param([string]$Text)
    if ($Typewriter -eq "1") {
        foreach ($line in ($Text -split "`n")) {
            $words = $line -split " "
            for ($w = 0; $w -lt $words.Count; $w++) {
                if ($w -gt 0) { Write-Host -NoNewline " " }
                Write-Host -NoNewline $words[$w]
                Start-Sleep -Milliseconds 15
            }
            Write-Host ""
        }
    } else {
        Write-Host $Text
    }
}

try {
    if (Test-Healthy) {
        Write-Host "radiant-llm is already running." -ForegroundColor Green
    } else {
        Write-Host -NoNewline "radiant-llm is not running" -ForegroundColor Yellow
        Write-Host " -- starting it now..."
        $composeArgs = @("-f", "$ScriptDir\docker-compose.yml")
        if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
            Write-Host "GPU detected -- starting with GPU acceleration" -ForegroundColor Green
            $composeArgs += @("-f", "$ScriptDir\docker-compose.gpu.yml")
        } else {
            Write-Host "No GPU detected -- starting CPU-only" -ForegroundColor DarkGray
        }
        docker compose @composeArgs up -d

        $healthy = $false
        Set-CursorVisible $false
        try {
            for ($attempt = 1; $attempt -le 60; $attempt++) {
                if (Test-Healthy) { $healthy = $true; break }
                $i = ($attempt - 1) % $SpinFrames.Count
                Write-Host -NoNewline "`r"
                Write-Host -NoNewline -ForegroundColor Yellow $SpinFrames[$i]
                Write-Host -NoNewline " Waiting for it to become healthy... "
                Write-Host -NoNewline -ForegroundColor DarkGray "($($attempt * 2)s)"
                Start-Sleep -Seconds 2
            }
        } finally {
            Clear-Line
            Set-CursorVisible $true
        }

        if ($healthy) {
            Write-Host "Container is healthy." -ForegroundColor Green
        } else {
            Write-Host "Container did not become healthy in time." -ForegroundColor Red
            Write-Host "Check logs with:"
            Write-Host "  docker compose logs -f"
            exit 1
        }
    }

    Write-Host "Connected to RADIANT-LLM at $Base" -ForegroundColor Green

    $settings = Invoke-RestMethod -Uri "$Base/model-settings" -TimeoutSec 5
    if ($settings.model_initialized -ne $true) {
        Write-Host ""
        Write-Host "No model is initialized yet on this container."
        $modelName = Read-Host "Model name to initialize (e.g. gpt-5.5)"
        $initResult = Invoke-ApiWithSpinner -Uri "$Base/initialize" -Method Post -BodyObject @{ model = $modelName } -Message "Initializing $modelName"
        if ($initResult.status -ne "ok") {
            Write-Host "Initialization failed:" -ForegroundColor Red
            $initResult | ConvertTo-Json -Depth 10 | Write-Host
            exit 1
        }
        Write-Host "Model '$modelName' initialized." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Chatting with RADIANT-LLM. Type 'exit' or 'quit' to stop chatting" -NoNewline
    Write-Host ""
    Write-Host "(the container itself keeps running afterward -- stop it with"
    Write-Host "'docker compose down' when you're done)."
    Write-Host "'/model <name>' switches models (e.g. /model gpt-6-astra),"
    Write-Host "'/typewriter' toggles the typing animation."
    Write-Host "Note: switching models clears the current conversation memory," -ForegroundColor DarkGray
    Write-Host "same as clicking Initialize again in the web UI." -ForegroundColor DarkGray
    Write-Host ""
    Write-Hr

    while ($true) {
        Write-Host -NoNewline "You: " -ForegroundColor Cyan
        $message = Read-Host

        if ([string]::IsNullOrWhiteSpace($message) -or $message -eq "exit" -or $message -eq "quit") {
            break
        }

        if ($message -like "/model *") {
            $newModel = $message.Substring(7)
            $initResult = Invoke-ApiWithSpinner -Uri "$Base/initialize" -Method Post -BodyObject @{ model = $newModel } -Message "Switching to $newModel"
            if ($initResult.status -eq "ok") {
                Write-Host "Switched to model '$newModel' (conversation memory reset)." -ForegroundColor Green
            } else {
                Write-Host "Could not switch model:" -ForegroundColor Red
                $initResult | ConvertTo-Json -Depth 10 | Write-Host
            }
            Write-Host ""
            Write-Hr
            continue
        }

        if ($message -eq "/typewriter") {
            if ($Typewriter -eq "1") {
                $Typewriter = "0"
                Write-Host "Typewriter effect: off" -ForegroundColor DarkGray
            } else {
                $Typewriter = "1"
                Write-Host "Typewriter effect: on" -ForegroundColor DarkGray
            }
            Write-Host ""
            Write-Hr
            continue
        }

        $result = Invoke-ApiWithSpinner -Uri "$Base/query" -Method Post -BodyObject @{ query = $message } -Message "RADIANT-LLM is thinking" -TimeoutSec 300

        $errorText = if ($result.detail) { $result.detail } elseif ($result.error) { $result.error } else { $null }
        if ($errorText) {
            Write-Host -NoNewline "RADIANT-LLM (error): " -ForegroundColor Red
            Write-Host $errorText
            Write-Host ""
            Write-Hr
            continue
        }

        $response = if ($null -ne $result.response) { $result.response } else { "(no response field in reply)" }
        Write-Host -NoNewline "RADIANT-LLM" -ForegroundColor Green
        Write-Host -NoNewline " "
        Write-Host "(${ThinkElapsed}s)" -ForegroundColor DarkGray
        Write-Typewriter $response
        Write-Host ""
        Write-Hr
    }

    Write-Host "Goodbye. Container is still running -- stop it with:"
    Write-Host "  docker compose down"
} finally {
    Set-CursorVisible $true
}
