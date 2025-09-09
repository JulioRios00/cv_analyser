#!/bin/bash
# Format code manually
# This script runs the same tools as pre-commit but manually

echo "🧹 Running code formatters..."

echo "📝 Running Black (formatter)..."
.venv/bin/black --line-length 79 src/ main.py

echo "📦 Running isort (import sorter)..."
.venv/bin/isort --profile black --line-length 79 src/ main.py

echo "🔍 Running flake8 (linter)..."
.venv/bin/flake8 --max-line-length=79 --extend-ignore=E203,W503 src/ main.py

echo "✅ Code formatting complete!"
echo "💡 Tip: Use 'pre-commit run --all-files' to run all hooks"
