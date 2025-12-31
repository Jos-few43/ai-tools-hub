#!/bin/bash
# PostToolUse hook - Auto-format code after edits

TOOL_NAME="$1"
FILE_PATH="$2"

if [[ "$TOOL_NAME" =~ (Write|Edit) && -f "$FILE_PATH" ]]; then
    # Format based on file type
    case "$FILE_PATH" in
        *.js|*.ts)
            if command -v prettier > /dev/null; then
                prettier --write "$FILE_PATH" 2>/dev/null
                echo "Formatted with Prettier"
            fi
            ;;
        *.py)
            if command -v black > /dev/null; then
                black "$FILE_PATH" 2>/dev/null
                echo "Formatted with Black"
            fi
            ;;
        *.go)
            if command -v gofmt > /dev/null; then
                gofmt -w "$FILE_PATH" 2>/dev/null
                echo "Formatted with gofmt"
            fi
            ;;
    esac
fi
