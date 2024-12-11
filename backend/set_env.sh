#!/usr/bin/env zsh

# Check if a file path is provided
if [[ -z "$1" ]]; then
  echo "Usage: $0 <path-to-env-file>"
  exit 1
fi

# Check if the file exists
if [[ ! -f "$1" ]]; then
  echo "Error: File not found: $1"
  exit 1
fi

# Export variables from the file to the current shell
set -a  # Automatically export all variables
source "$1"
set +a

echo "Environment variables exported from $1"
