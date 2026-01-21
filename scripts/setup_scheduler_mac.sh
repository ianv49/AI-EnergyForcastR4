#!/bin/bash
# macOS Launchd setup for automated sensor ingestion
# This script creates a LaunchAgent that runs the ingestion every 5 minutes

set -e

REPO_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PLIST_FILE="$HOME/Library/LaunchAgents/com.energy.sensor.ingestion.plist"
SCRIPT_PATH="$REPO_DIR/run_ingest.py"
VENV_PATH="$REPO_DIR/.venv/bin/python3"

echo "Creating LaunchAgent for automated ingestion..."
echo "Repo directory: $REPO_DIR"
echo "Script path: $SCRIPT_PATH"
echo "Venv Python: $VENV_PATH"

# Create plist file
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.energy.sensor.ingestion</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$VENV_PATH</string>
        <string>$SCRIPT_PATH</string>
    </array>
    
    <key>StartInterval</key>
    <integer>300</integer>
    
    <key>WorkingDirectory</key>
    <string>$REPO_DIR</string>
    
    <key>StandardOutPath</key>
    <string>$REPO_DIR/logs/ingestion.stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>$REPO_DIR/logs/ingestion.stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/opt/postgresql@15/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

echo "✓ Plist file created at: $PLIST_FILE"

# Load the LaunchAgent
launchctl load "$PLIST_FILE"
echo "✓ LaunchAgent loaded. Ingestion will run every 5 minutes."

# List loaded services
echo ""
echo "Active LaunchAgents:"
launchctl list | grep energy.sensor || echo "Not yet active (may take a moment to start)"

echo ""
echo "To unload: launchctl unload $PLIST_FILE"
echo "To view logs: tail -f $REPO_DIR/logs/ingestion*.log"
