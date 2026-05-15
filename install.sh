#!/usr/bin/env bash
set -e

echo "=========================================="
echo "          Installing k8sh...              "
echo "=========================================="

INSTALL_DIR="$HOME/.k8sh"

# 1. Create installation directory
echo "=> Creating installation directory at $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 2. Get project files
if [ -f "./init.py" ] && [ -f "./main.py" ]; then
    echo "=> Local copy detected. Copying project files..."
    cp -R ./* "$INSTALL_DIR/"
else
    echo "=> Downloading latest version from GitHub..."
    git clone https://github.com/AndoniSalcedo/k8sh.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 3. Setup python virtual environment
echo "=> Setting up virtual environment..."
if ! python3 -m venv "$INSTALL_DIR/venv" > /dev/null 2>&1; then
    echo ""
    echo "❌ ERROR: Failed to create virtual environment."
    echo "It seems 'python3-venv' is not installed on your system (very common on Ubuntu/Debian)."
    echo "Please install it by running the following command:"
    echo ""
    echo "    sudo apt update && sudo apt install -y python3-venv"
    echo ""
    echo "After installing it, simply run this installation command again!"
    exit 1
fi

echo "=> Installing dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip > /dev/null 2>&1
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt" > /dev/null 2>&1

# 4. Detect shell configuration file
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
else
    # Fallback
    RC_FILE="$HOME/.profile"
fi

echo "=> Configuring alias for $SHELL_NAME ($RC_FILE)..."
ALIAS_CMD="alias k8sh='\"$INSTALL_DIR/venv/bin/python\" \"$INSTALL_DIR/init.py\"'"

# 5. Remove previous alias if it exists and inject the new one
touch "$RC_FILE"
if grep -q "alias k8sh=" "$RC_FILE"; then
    grep -v "alias k8sh=" "$RC_FILE" > "${RC_FILE}.tmp"
    mv "${RC_FILE}.tmp" "$RC_FILE"
fi

echo "" >> "$RC_FILE"
echo "# k8sh command alias" >> "$RC_FILE"
echo "$ALIAS_CMD" >> "$RC_FILE"

echo "=========================================="
echo "   k8sh installed successfully! 🎉        "
echo "=========================================="
echo "To start using it right now, run:"
echo "    source $RC_FILE"
echo "Then simply type: k8sh"
