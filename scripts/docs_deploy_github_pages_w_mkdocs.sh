#!/bin/bash
"""
This script is used to deploy documentation to GitHub Pages using mkdocs.
It first copies the contents of docs/index.md to README.md, and then runs mkdocs gh-deploy to publish the documentation.
It is important to run this script with bash, not sh.
It also ensures that the script is run from the correct directory and handles errors appropriately.
It is assumed that mkdocs is already installed and configured in the environment.
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
    # Change to parent directory
    if cd ..; then
        echo "Successfully changed to parent directory: $(pwd)"
    else
        echo "Failed to change to parent directory" >&2
        exit 1
    fi
else
    echo "Failed to change to script directory" >&2
    exit 1
fi

echo "Current working directory: $(pwd)"

# Overwrite the root-level README.md file
echo ""
echo "Copying docs/index.md to README.md (i.e. overwriting README.md)..."
cp ./docs/index.md ./README.md

echo "Activating poetry environment..."
# poetry env activate

# Publish the docs to GitHub Pages
echo ""
echo "Running mkdocs gh-deploy to 'gh-pages' branch..."
poetry run mkdocs gh-deploy --config-file ./mkdocs.yml
