#!/usr/bin/env bash
# Trigger one isolated scraper-host run, pull sanitized JSONL back, and build a
# World Side forecast for the console. This script is intentionally key-auth
# only: if the scraper host asks for a password, the workflow fails closed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SCRAPER_SSH_TARGET="${SCRAPER_SSH_TARGET:-prophet-scraper}"
SCRAPER_REMOTE_APP="${SCRAPER_REMOTE_APP:-/srv/scraper/app}"
SCRAPER_REMOTE_OUTPUT="${SCRAPER_REMOTE_OUTPUT:-/srv/scraper/output}"
SCRAPER_LIVE="${SCRAPER_LIVE:-1}"
SCRAPER_LIMIT="${SCRAPER_LIMIT:-25}"
SCRAPER_MAX_RECORDS="${SCRAPER_MAX_RECORDS:-500}"
SCRAPER_TIMEOUT="${SCRAPER_TIMEOUT:-20}"
PROPHET_DEPLOY_SCRAPER="${PROPHET_DEPLOY_SCRAPER:-0}"

LOCAL_INCOMING_DIR="${LOCAL_INCOMING_DIR:-$REPO_ROOT/world-side/data/chatter/incoming/console}"
LOCAL_FORECAST_OUT="${LOCAL_FORECAST_OUT:-$REPO_ROOT/world-side/outputs/runtime/live-scraper-forecast-edge-appliance.json}"
CANDIDATE_FILE="${CANDIDATE_FILE:-$REPO_ROOT/world-side/fixtures/exploit-candidate-edge-appliance.json}"

RUN_ID="${SCRAPER_RUN_ID:-console-$(date -u '+%Y%m%dT%H%M%SZ')}"
LOCAL_CHATTER_FILE="$LOCAL_INCOMING_DIR/sanitized-$RUN_ID.jsonl"
LOCAL_MANIFEST_FILE="$LOCAL_INCOMING_DIR/sanitization-manifest-$RUN_ID.json"

log() {
    printf '[%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*"
}

fail() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

ssh_batch() {
    ssh \
        -o BatchMode=yes \
        -o NumberOfPasswordPrompts=0 \
        -o ConnectTimeout=8 \
        "$SCRAPER_SSH_TARGET" \
        "$@"
}

require_file() {
    local label="$1"
    local path="$2"
    [ -f "$path" ] || fail "$label not found: $path"
}

require_file "candidate file" "$CANDIDATE_FILE"
mkdir -p "$LOCAL_INCOMING_DIR" "$(dirname "$LOCAL_FORECAST_OUT")"

log "Checking key-based SSH to $SCRAPER_SSH_TARGET"
ssh_batch "printf 'prophet-scraper-ready\n'" >/dev/null

if [ "$PROPHET_DEPLOY_SCRAPER" = "1" ]; then
    log "Deploying scraper package to $SCRAPER_SSH_TARGET:$SCRAPER_REMOTE_APP"
    rsync -az --delete \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env.local' \
        --exclude='secrets/' \
        "$REPO_ROOT/world-side/scraper/" \
        "$SCRAPER_SSH_TARGET:$SCRAPER_REMOTE_APP/"

    log "Bootstrapping scraper host package"
    ssh_batch "bash '$SCRAPER_REMOTE_APP/bin/bootstrap-scraper-machine.sh'"
fi

log "Running isolated scraper workflow on $SCRAPER_SSH_TARGET"
ssh_batch \
    "SCRAPER_RUN_ID='$RUN_ID' SCRAPER_LIVE='$SCRAPER_LIVE' SCRAPER_LIMIT='$SCRAPER_LIMIT' SCRAPER_MAX_RECORDS='$SCRAPER_MAX_RECORDS' SCRAPER_TIMEOUT='$SCRAPER_TIMEOUT' bash '$SCRAPER_REMOTE_APP/bin/run-once.sh'"

log "Pulling sanitized output only"
rsync -az \
    -e "ssh -o BatchMode=yes -o NumberOfPasswordPrompts=0" \
    "$SCRAPER_SSH_TARGET:$SCRAPER_REMOTE_OUTPUT/sanitized-$RUN_ID.jsonl" \
    "$LOCAL_CHATTER_FILE"

rsync -az \
    -e "ssh -o BatchMode=yes -o NumberOfPasswordPrompts=0" \
    "$SCRAPER_SSH_TARGET:$SCRAPER_REMOTE_OUTPUT/sanitization-manifest-$RUN_ID.json" \
    "$LOCAL_MANIFEST_FILE"

log "Building validated forecast from sanitized chatter"
PYTHONPATH="$REPO_ROOT/world-side" python3 -m forecaster.cli \
    --candidate "$CANDIDATE_FILE" \
    --chatter "$LOCAL_CHATTER_FILE" \
    --out "$LOCAL_FORECAST_OUT"

printf 'PROPHET_RUN_ID=%s\n' "$RUN_ID"
printf 'PROPHET_CHATTER_FILE=%s\n' "$LOCAL_CHATTER_FILE"
printf 'PROPHET_MANIFEST_FILE=%s\n' "$LOCAL_MANIFEST_FILE"
printf 'PROPHET_FORECAST_FILE=%s\n' "$LOCAL_FORECAST_OUT"
