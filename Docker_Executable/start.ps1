# RADIANT-LLM -- start script (auto-detects GPU, no manual -f flags needed)
#
# Usage: .\start.ps1
#
# Replaces plain `docker compose up -d`. Automatically applies
# docker-compose.gpu.yml when an NVIDIA GPU is present on this machine
# (detected via `nvidia-smi`), otherwise starts CPU-only -- either way,
# a single command, no flags to remember.
#
# Always operates on the compose files sitting next to this script
# ($PSScriptRoot), so it works the same whether you're sitting in this
# folder or invoking it by full path from somewhere else.

$composeArgs = @("-f", "$PSScriptRoot\docker-compose.yml")

if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    Write-Host "GPU detected -- starting with GPU acceleration" -ForegroundColor Green
    $composeArgs += @("-f", "$PSScriptRoot\docker-compose.gpu.yml")
} else {
    Write-Host "No GPU detected -- starting CPU-only" -ForegroundColor Yellow
}

docker compose @composeArgs up -d
