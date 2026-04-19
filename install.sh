#!/bin/bash
# archive-librarian — one-command install for macOS
# Run from inside the archive-librarian/ folder:
#   ./install.sh
#
# What it does:
#   1. Checks Python 3.11+ is available (suggests install if not)
#   2. Creates a venv inside this folder
#   3. Installs Python dependencies
#   4. Installs `librarian` as a command in /usr/local/bin (or ~/.local/bin)
#   5. Runs the interactive setup walkthrough

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

cd "$(dirname "$0")"
ROOT="$(pwd)"

echo -e "\n${CYAN}${BOLD}━━━ archive-librarian setup ━━━${NC}\n"

# --- Step 1: Check Python ---
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        VERSION=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
        MAJOR=$(echo "$VERSION" | cut -d. -f1)
        MINOR=$(echo "$VERSION" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
            PYTHON="$candidate"
            echo -e "${GREEN}✓${NC} Python $VERSION found ($candidate)"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED}✗${NC} Python 3.11 or newer is required."
    echo -e "  Install with Homebrew: ${BOLD}brew install python@3.13${NC}"
    echo -e "  Or download from:      ${BOLD}https://www.python.org/downloads/${NC}"
    exit 1
fi

# --- Step 2: Create venv ---
if [ ! -d "$ROOT/.venv" ]; then
    echo -e "${CYAN}→${NC} Creating Python virtual environment..."
    "$PYTHON" -m venv "$ROOT/.venv"
fi
source "$ROOT/.venv/bin/activate"
echo -e "${GREEN}✓${NC} Virtual environment ready"

# --- Step 3: Install deps ---
echo -e "${CYAN}→${NC} Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r "$ROOT/requirements.txt"
echo -e "${GREEN}✓${NC} Dependencies installed"

# --- Step 4: Install `librarian` command ---
chmod +x "$ROOT/librarian"

# Determine install location
INSTALL_BIN=""
if [ -w "/usr/local/bin" ]; then
    INSTALL_BIN="/usr/local/bin"
elif [ -d "$HOME/.local/bin" ] || mkdir -p "$HOME/.local/bin" 2>/dev/null; then
    INSTALL_BIN="$HOME/.local/bin"
fi

if [ -n "$INSTALL_BIN" ]; then
    # Create a thin shim that activates the venv before running librarian
    SHIM="$INSTALL_BIN/librarian"
    cat > "$SHIM" <<EOF
#!/bin/bash
source "$ROOT/.venv/bin/activate"
exec python "$ROOT/librarian" "\$@"
EOF
    chmod +x "$SHIM"
    echo -e "${GREEN}✓${NC} Installed command: ${BOLD}librarian${NC} (at $SHIM)"

    # Check if INSTALL_BIN is in PATH
    if ! echo ":$PATH:" | grep -q ":$INSTALL_BIN:"; then
        echo -e "${YELLOW}!${NC} ${BOLD}$INSTALL_BIN${NC} is not in your PATH."
        echo -e "  Add this line to your shell config (~/.zshrc or ~/.bashrc):"
        echo -e "  ${BOLD}export PATH=\"$INSTALL_BIN:\$PATH\"${NC}"
        echo -e "  Then run: ${BOLD}source ~/.zshrc${NC} (or restart your terminal)"
    fi
else
    echo -e "${YELLOW}!${NC} Could not install global command. Run from this folder with:"
    echo -e "  ${BOLD}./librarian <command>${NC}"
fi

# --- Step 5: Run interactive setup ---
echo
echo -e "${CYAN}${BOLD}━━━ Starting interactive setup ━━━${NC}"
echo
"$ROOT/.venv/bin/python" "$ROOT/librarian" setup
