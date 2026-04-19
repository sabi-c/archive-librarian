#!/bin/bash
# Clean demo recording — quits noisy apps, positions the window deterministically,
# records only the window's screen region (no full-screen capture so other dialogs
# can't intrude even if they appear).
#
# Usage: ./clean_demo_record.sh [duration_seconds] [output_path]

set -e

DURATION="${1:-38}"
OUTPUT="${2:-/Users/seb/Downloads/Manual Library/Seb's Mind/Seb's Mind/Note inbox/archive-librarian-clean-demo.mov}"

# --- Step 1: Quit (not hide) noisy apps that pop dialogs ---
echo "→ Quitting noisy apps..."
for app in "Dropbox" "Slack" "Mail" "Calendar" "Reminders" "Google Drive"; do
    osascript -e "try
        tell application \"$app\" to quit
    end try" 2>/dev/null || true
done

# --- Step 2: Enable Do Not Disturb to suppress notifications ---
echo "→ Enabling Do Not Disturb (Focus mode)..."
osascript -e 'tell application "System Events" to keystroke "d" using {control down, option down, command down}' 2>/dev/null || true
sleep 0.5

# --- Step 3: Kill any stale demo / app processes ---
pkill -9 -f "Archive Librarian" 2>/dev/null || true
pkill -9 -f "demo_recorder" 2>/dev/null || true
pkill -9 -f "webview_app" 2>/dev/null || true
sleep 1

# --- Step 4: Launch demo, then move + size + position window deterministically ---
echo "→ Launching app for window-position lock..."
cd "$(dirname "$0")"
source .venv/bin/activate
python demo_recorder.py >/dev/null 2>&1 &
DEMO_PID=$!
sleep 3  # let window appear

# Position window at known location: x=100 y=80, size 1100x900
# This bounds the recording region precisely.
WIN_X=100
WIN_Y=80
WIN_W=1100
WIN_H=900

osascript <<EOF 2>/dev/null
tell application "System Events"
    repeat with p in (every process whose name contains "Archive Librarian")
        try
            set position of front window of p to {$WIN_X, $WIN_Y}
            set size of front window of p to {$WIN_W, $WIN_H}
        end try
    end repeat
end tell
EOF
sleep 0.5

# --- Step 5: Record JUST the window region using ffmpeg ---
# avfoundation Capture screen 0 = device "1:none"
# Crop to the window region. macOS captures at 2x for retina, so multiply.
SCALE=2
CROP_W=$((WIN_W * SCALE))
CROP_H=$((WIN_H * SCALE))
CROP_X=$((WIN_X * SCALE))
CROP_Y=$((WIN_Y * SCALE))

# Kill the demo we already launched — we'll restart it inside the recording window
kill $DEMO_PID 2>/dev/null || true
pkill -f "demo_recorder" 2>/dev/null || true
sleep 1

echo "→ Recording $DURATION sec, cropped to window region (${WIN_W}x${WIN_H} at $WIN_X,$WIN_Y)..."
rm -f "$OUTPUT"

# Web/QuickTime/iOS-compatible H.264 baseline + faststart for streaming.
# avfoundation captures via uyvy422; we yuv420p convert in the same pipeline.
ffmpeg -hide_banner -loglevel error \
    -f avfoundation -framerate 30 -capture_cursor 0 -i "1:none" \
    -t "$DURATION" \
    -vf "crop=${CROP_W}:${CROP_H}:${CROP_X}:${CROP_Y},scale=${WIN_W}:${WIN_H},format=yuv420p" \
    -c:v libx264 -preset medium -profile:v baseline -level 3.1 \
    -pix_fmt yuv420p -movflags +faststart -an \
    "$OUTPUT" &
RECORD_PID=$!
sleep 2  # let ffmpeg start

# Restart the demo (window will land at same x,y because of macOS positioning memory)
python demo_recorder.py >/dev/null 2>&1 &
DEMO_PID=$!

# Wait for recording to finish
wait $RECORD_PID 2>/dev/null
echo "→ Recording complete."

# Cleanup
kill $DEMO_PID 2>/dev/null || true
pkill -f "demo_recorder" 2>/dev/null || true
pkill -f "Archive Librarian" 2>/dev/null || true

echo "→ Output: $OUTPUT"
ls -lh "$OUTPUT"
