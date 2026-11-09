#!/bin/bash
# RADIANT-LLM -- all-in-one: starts the container if it isn't already running
# (same as ./start.sh, auto-detecting GPU), waits for it to be healthy, then
# drops straight into a terminal chat loop against it.
#
# Usage: ./radiant_llm_cli_chat.sh
#
# This does NOT stop the container when you exit the chat (type "exit"/
# "quit"/Ctrl+C) -- it keeps running in the background afterward, same as
# if you'd started it with ./start.sh. Stop it yourself whenever you're done:
#   docker compose down
#
# In the chat: "/model <name>" switches models, "/typewriter" toggles the
# typing animation. Set RADIANT_LLM_TYPEWRITER=0 before launching to start
# with it off.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8060
BASE="http://localhost:${PORT}"
TYPEWRITER="${RADIANT_LLM_TYPEWRITER:-1}"

if ! command -v jq >/dev/null 2>&1; then
    echo "This script needs 'jq' to build/parse JSON. Install it with: sudo apt install jq"
    exit 1
fi

# ── appearance ───────────────────────────────────────────────────────────
supports_color() {
    [ -t 1 ] && command -v tput >/dev/null 2>&1 && [ "$(tput colors 2>/dev/null || printf 0)" -ge 8 ]
}

if supports_color; then
    C_RESET="$(tput sgr0 2>/dev/null || true)"
    C_BOLD="$(tput bold 2>/dev/null || true)"
    C_DIM="$(tput dim 2>/dev/null || true)"
    C_CYAN="$(tput setaf 6 2>/dev/null || true)"
    C_GREEN="$(tput setaf 2 2>/dev/null || true)"
    C_YELLOW="$(tput setaf 3 2>/dev/null || true)"
    C_RED="$(tput setaf 1 2>/dev/null || true)"
else
    C_RESET=""; C_BOLD=""; C_DIM=""; C_CYAN=""; C_GREEN=""; C_YELLOW=""; C_RED=""
fi

cleanup_cursor() { tput cnorm 2>/dev/null || true; }
trap cleanup_cursor EXIT

SPIN_FRAMES=(⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏)
THINK_ELAPSED=0
HR_LINE="────────────────────────────────────────────────────────"

hr() { printf "%s%s%s\n" "$C_DIM" "$HR_LINE" "$C_RESET"; }

spin_wait() {
    # $1 = pid to wait on, $2 = status message. Sets THINK_ELAPSED on return.
    local pid="$1" msg="$2" start elapsed i=0
    start=$SECONDS
    tput civis 2>/dev/null || true
    while kill -0 "$pid" 2>/dev/null; do
        elapsed=$((SECONDS - start))
        printf "\r%s%s%s %s... %s(%ss)%s" "$C_YELLOW" "${SPIN_FRAMES[$i]}" "$C_RESET" "$msg" "$C_DIM" "$elapsed" "$C_RESET"
        i=$(( (i + 1) % ${#SPIN_FRAMES[@]} ))
        sleep 0.1
    done
    printf "\r\033[K"
    tput cnorm 2>/dev/null || true
    THINK_ELAPSED=$((SECONDS - start))
}

type_out() {
    # $1 = text. Reveals word-by-word if TYPEWRITER=1 and stdout is a tty.
    local text="$1" line word first
    if [ "$TYPEWRITER" = "1" ] && [ -t 1 ]; then
        while IFS= read -r line; do
            first=1
            for word in $line; do
                if [ "$first" = 1 ]; then printf "%s" "$word"; first=0
                else printf " %s" "$word"; fi
                sleep 0.015
            done
            printf "\n"
        done <<< "$text"
    else
        printf "%s\n" "$text"
    fi
}

is_healthy() {
    curl -s -o /dev/null -w "" --max-time 3 "${BASE}/health" 2>/dev/null
}

if is_healthy; then
    echo "${C_GREEN}radiant-llm is already running.${C_RESET}"
else
    echo "${C_YELLOW}radiant-llm is not running${C_RESET} -- starting it now..."
    COMPOSE_ARGS=(-f "$SCRIPT_DIR/docker-compose.yml")
    if command -v nvidia-smi >/dev/null 2>&1; then
        echo "${C_GREEN}GPU detected${C_RESET} -- starting with GPU acceleration"
        COMPOSE_ARGS+=(-f "$SCRIPT_DIR/docker-compose.gpu.yml")
    else
        echo "${C_DIM}No GPU detected${C_RESET} -- starting CPU-only"
    fi
    docker compose "${COMPOSE_ARGS[@]}" up -d

    i=0
    HEALTHY=0
    tput civis 2>/dev/null || true
    for attempt in $(seq 1 60); do
        if is_healthy; then
            HEALTHY=1
            break
        fi
        printf "\r%s%s%s Waiting for it to become healthy... %s(%ss)%s" "$C_YELLOW" "${SPIN_FRAMES[$i]}" "$C_RESET" "$C_DIM" "$((attempt * 2))" "$C_RESET"
        i=$(( (i + 1) % ${#SPIN_FRAMES[@]} ))
        sleep 2
    done
    printf "\r\033[K"
    tput cnorm 2>/dev/null || true

    if [ "$HEALTHY" = "1" ]; then
        echo "${C_GREEN}Container is healthy.${C_RESET}"
    else
        echo "${C_RED}Container did not become healthy in time.${C_RESET} Check logs with:"
        echo "  docker compose logs -f"
        exit 1
    fi
fi

echo "${C_GREEN}Connected to RADIANT-LLM at ${BASE}${C_RESET}"

INITIALIZED="$(curl -s --max-time 5 "${BASE}/model-settings" | jq -r '.model_initialized')"
if [ "$INITIALIZED" != "true" ]; then
    echo ""
    echo "No model is initialized yet on this container."
    read -r -p "Model name to initialize (e.g. gpt-5.5): " MODEL_NAME
    RESP_FILE="$(mktemp)"
    curl -s --max-time 60 -X POST "${BASE}/initialize" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg m "$MODEL_NAME" '{model: $m}')" > "$RESP_FILE" &
    CURL_PID=$!
    spin_wait "$CURL_PID" "Initializing ${MODEL_NAME}"
    wait "$CURL_PID"
    INIT_RESULT="$(cat "$RESP_FILE")"
    rm -f "$RESP_FILE"
    INIT_OK="$(echo "$INIT_RESULT" | jq -r '.status // empty')"
    if [ "$INIT_OK" != "ok" ]; then
        echo "${C_RED}Initialization failed:${C_RESET}"
        echo "$INIT_RESULT" | jq .
        exit 1
    fi
    echo "${C_GREEN}Model '${MODEL_NAME}' initialized.${C_RESET}"
fi

echo ""
echo "${C_BOLD}Chatting with RADIANT-LLM.${C_RESET} Type 'exit' or 'quit' to stop chatting"
echo "(the container itself keeps running afterward -- stop it with"
echo "'docker compose down' when you're done)."
echo "'${C_BOLD}/model <name>${C_RESET}' switches models (e.g. /model gpt-6-astra),"
echo "'${C_BOLD}/typewriter${C_RESET}' toggles the typing animation."
echo "${C_DIM}Note: switching models clears the current conversation memory,"
echo "same as clicking Initialize again in the web UI.${C_RESET}"
echo ""
hr

PROMPT="$(printf '%s%sYou:%s ' "$C_BOLD" "$C_CYAN" "$C_RESET")"

while true; do
    read -r -p "$PROMPT" MESSAGE || break
    case "$MESSAGE" in
        ""|exit|quit) break ;;
        /model\ *)
            NEW_MODEL="${MESSAGE#/model }"
            RESP_FILE="$(mktemp)"
            curl -s --max-time 60 -X POST "${BASE}/initialize" \
                -H "Content-Type: application/json" \
                -d "$(jq -n --arg m "$NEW_MODEL" '{model: $m}')" > "$RESP_FILE" &
            CURL_PID=$!
            spin_wait "$CURL_PID" "Switching to ${NEW_MODEL}"
            wait "$CURL_PID"
            INIT_RESULT="$(cat "$RESP_FILE")"
            rm -f "$RESP_FILE"
            INIT_OK="$(echo "$INIT_RESULT" | jq -r '.status // empty')"
            if [ "$INIT_OK" = "ok" ]; then
                echo "${C_GREEN}Switched to model '${NEW_MODEL}' (conversation memory reset).${C_RESET}"
            else
                echo "${C_RED}Could not switch model:${C_RESET}"
                echo "$INIT_RESULT" | jq .
            fi
            echo ""
            hr
            continue
            ;;
        /typewriter)
            if [ "$TYPEWRITER" = "1" ]; then
                TYPEWRITER=0
                echo "${C_DIM}Typewriter effect: off${C_RESET}"
            else
                TYPEWRITER=1
                echo "${C_DIM}Typewriter effect: on${C_RESET}"
            fi
            echo ""
            hr
            continue
            ;;
    esac

    RESP_FILE="$(mktemp)"
    curl -s --max-time 300 -X POST "${BASE}/query" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg q "$MESSAGE" '{query: $q}')" > "$RESP_FILE" &
    CURL_PID=$!
    spin_wait "$CURL_PID" "RADIANT-LLM is thinking"
    wait "$CURL_PID"
    RESULT="$(cat "$RESP_FILE")"
    rm -f "$RESP_FILE"

    ERROR="$(echo "$RESULT" | jq -r '.detail // .error // empty')"
    if [ -n "$ERROR" ]; then
        echo "${C_RED}RADIANT-LLM (error):${C_RESET} $ERROR"
        echo ""
        hr
        continue
    fi

    RESPONSE="$(echo "$RESULT" | jq -r '.response // "(no response field in reply)"')"
    echo "${C_BOLD}${C_GREEN}RADIANT-LLM${C_RESET} ${C_DIM}(${THINK_ELAPSED}s)${C_RESET}"
    type_out "$RESPONSE"
    echo ""
    hr
done

echo "Goodbye. Container is still running -- stop it with:"
echo "  docker compose down"
