#!/bin/bash
# Double-click this file to install Archive Librarian.
# It will open Terminal automatically (that's normal — macOS opens .command files in Terminal).

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# Get the directory of this script (works even when double-clicked)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

clear
cat <<EOF

${CYAN}${BOLD}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         📚  ARCHIVE LIBRARIAN — Setup Installer  📚       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝${NC}

${BOLD}What's about to happen:${NC}

  1. We'll check that Python is installed (and help you install it if not)
  2. We'll set up a private workspace for the app inside this folder
  3. We'll add a "Download Book" shortcut to your Desktop
  4. We'll launch a friendly setup wizard with native Mac dialogs

  Total time: about 3 minutes.

  ${YELLOW}Don't worry about the text scrolling by — that's normal.
  All the questions will pop up as native Mac dialog boxes.${NC}

EOF

read -p "Press Enter to begin..."

# ---------------------------------------------------------------------------
# Step 1: Check Python
# ---------------------------------------------------------------------------
echo
echo -e "${CYAN}→ Checking for Python 3.11 or newer...${NC}"

PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        VERSION=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
            PYTHON="$candidate"
            echo -e "${GREEN}✓ Found Python $VERSION${NC}"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo
    echo -e "${YELLOW}⚠  Python 3.11 or newer is needed.${NC}"
    echo
    echo "We'll open the official Python download page in your browser."
    echo "Download the macOS installer (the .pkg file), open it, and click through the install."
    echo
    echo "When Python is installed, double-click 'Install Archive Librarian.command' again."
    echo
    osascript -e 'display dialog "Archive Librarian needs Python 3.11 or newer. Click OK and we will open the Python download page. Download the macOS installer (the .pkg file), install it, then double-click Install Archive Librarian.command again." with title "Python required" buttons {"OK"} default button "OK" with icon caution' 2>/dev/null || true
    open "https://www.python.org/downloads/"
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 2: Create venv & install deps
# ---------------------------------------------------------------------------
echo
echo -e "${CYAN}→ Setting up the app's private Python workspace...${NC}"
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    "$PYTHON" -m venv "$SCRIPT_DIR/.venv"
fi
source "$SCRIPT_DIR/.venv/bin/activate"
echo -e "${GREEN}✓ Workspace ready${NC}"

echo
echo -e "${CYAN}→ Installing dependencies (one-time, takes ~30 seconds)...${NC}"
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# ---------------------------------------------------------------------------
# Step 3: Make scripts executable & install command
# ---------------------------------------------------------------------------
chmod +x "$SCRIPT_DIR/librarian"
chmod +x "$SCRIPT_DIR/Install Archive Librarian.command"

# Install global librarian command if /usr/local/bin or ~/.local/bin is writable
INSTALL_BIN=""
if [ -w "/usr/local/bin" ] 2>/dev/null; then
    INSTALL_BIN="/usr/local/bin"
else
    mkdir -p "$HOME/.local/bin"
    INSTALL_BIN="$HOME/.local/bin"
fi

cat > "$INSTALL_BIN/librarian" <<EOF
#!/bin/bash
source "$SCRIPT_DIR/.venv/bin/activate"
exec python "$SCRIPT_DIR/librarian" "\$@"
EOF
chmod +x "$INSTALL_BIN/librarian"
echo -e "${GREEN}✓ 'librarian' command installed${NC}"

# ---------------------------------------------------------------------------
# Step 4: Create Desktop "Download Book" shortcut
# ---------------------------------------------------------------------------
echo
echo -e "${CYAN}→ Creating 'Download Book' shortcut on your Desktop...${NC}"
DESKTOP_SHORTCUT="$HOME/Desktop/Download Book.command"
cat > "$DESKTOP_SHORTCUT" <<EOF
#!/bin/bash
# Double-click to download a book from archive.org.
source "$SCRIPT_DIR/.venv/bin/activate"
cd "$SCRIPT_DIR"

URL=\$(osascript -e 'try
    set theAnswer to text returned of (display dialog "Paste the archive.org URL of the book you want to download:" with title "Download a Book" default answer "" buttons {"Cancel", "Download"} default button "Download" with icon note)
    return theAnswer
on error number -128
    return "__CANCELLED__"
end try' 2>/dev/null)

if [ "\$URL" = "__CANCELLED__" ] || [ -z "\$URL" ]; then
    echo "Cancelled."
    exit 0
fi

echo
echo "Downloading: \$URL"
echo "This can take a few minutes..."
echo
python "$SCRIPT_DIR/librarian" download "\$URL"
RC=\$?

if [ \$RC -eq 0 ]; then
    osascript -e "display dialog \"Book downloaded! Check your books folder.\" with title \"Done\" buttons {\"Open Books Folder\", \"OK\"} default button \"OK\" with icon note" 2>/dev/null
    BUTTON=\$(osascript -e 'button returned of result' 2>/dev/null)
    if [ "\$BUTTON" = "Open Books Folder" ]; then
        python "$SCRIPT_DIR/librarian" status > /dev/null
        # Open the configured library directory
        LIB=\$(python -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from config import get_library_dir; print(get_library_dir())")
        open "\$LIB"
    fi
else
    osascript -e 'display dialog "Download failed. See the Terminal window for details." with title "Download failed" buttons {"OK"} default button "OK" with icon stop' 2>/dev/null
fi

echo
echo "Press Enter to close this window."
read
EOF
chmod +x "$DESKTOP_SHORTCUT"
echo -e "${GREEN}✓ Desktop shortcut created${NC}"

# ---------------------------------------------------------------------------
# Step 5: Launch interactive setup
# ---------------------------------------------------------------------------
echo
echo -e "${CYAN}━━━ Launching setup wizard (look for dialog boxes!) ━━━${NC}"
echo
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/librarian" setup

echo
echo -e "${GREEN}${BOLD}━━━ Install complete ━━━${NC}"
echo
echo "  • Double-click 'Download Book' on your Desktop to grab a book"
echo "  • You can also type 'librarian' commands in Terminal if you want"
echo "  • This installer file (this folder) is needed for the app to work"
echo "    — keep it somewhere safe, don't trash it."
echo
echo "Press Enter to close this window."
read
