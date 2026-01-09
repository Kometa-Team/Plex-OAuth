# Dev Container Setup

This project includes a VS Code Dev Container configuration for consistent development environments.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Getting Started

1. **Open in Dev Container**:
   - Open this project in VS Code
   - Press `F1` or `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows/Linux)
   - Select `Dev Containers: Reopen in Container`
   - Wait for the container to build and setup to complete

2. **Start Development**:
   ```bash
   uv run python app.py
   ```

3. **Access the App**:
   - Open http://localhost:8080 in your browser
   - The port is automatically forwarded from the container

## What's Included

- **Python 3.11** - Matching production runtime
- **uv** - Fast Python package manager
- **VS Code Extensions**:
  - Python language support
  - Pylance for IntelliSense
  - Black formatter
  - Ruff linter
  - Docker support

## Features

- ✅ Automatic dependency installation
- ✅ Pre-configured environment variables
- ✅ Port forwarding (8080)
- ✅ Format on save
- ✅ Python testing support
- ✅ Git integration

## Customization

Edit [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) to:
- Add VS Code extensions
- Change Python version
- Configure additional ports
- Modify environment variables

## Troubleshooting

### Container won't start
- Ensure Docker Desktop is running
- Try rebuilding: `Dev Containers: Rebuild Container`

### Dependencies not installed
- Run manually: `uv sync`

### Can't access the app
- Check port forwarding in VS Code's Ports panel
- Ensure Flask is running on `0.0.0.0:8080`
