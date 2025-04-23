#!/bin/bash
"""
This script formats and lints the codebase.
"""

# If there's an error, stop the script
set -e
# Print each command that's executed
set -x

# Check if running with 'sh' or 'bash' (must be 'bash')
if [ -z "$BASH_VERSION" ]; then
    echo "Please run this script with bash, not sh"
    exit 1
fi

# Get the real path of the script, resolving any symlinks
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
# Get the directory containing the script
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# Try to change to the directory
if cd "$SCRIPT_DIR"; then
    echo "Successfully changed to script directory: $(pwd)"
else
    echo "Failed to change to script directory" >&2
    exit 1
fi

echo "Current working directory: $(pwd)"

# Use Ruff to lint everything
echo ""
echo "Running ruff linter..."
# Run the linter
ruff check ../src --fix --config ../pyproject.toml
ruff check ../tests --fix --config ../pyproject.toml

# Run the formatter
echo ""
echo "Running ruff formatter..."
ruff format ../src --config ../pyproject.toml
ruff format ../tests --config ../pyproject.toml

# # Run the pyright linter (takes a bit longer)
# echo ""
# echo "Running pyright linter..."
# pyright ../src --project ../pyproject.toml
# pyright ../tests --project ../pyproject.toml
