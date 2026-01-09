# Plex-OAuth Project

## Project Overview
This is a Flask web application for Plex OAuth authentication. Users can authenticate with Plex and receive an access token for use with Kometa.

## Tech Stack
- **Framework**: Flask
- **Package Manager**: uv
- **Deployment**: Heroku
- **Python Version**: 3.11

## Development
- Use `uv sync` to install dependencies
- Use `uv run python app.py` to run locally
- Environment variables are in `.env` (local) or Heroku config (production)

## Deployment
- Deployed to Heroku using `git push heroku main`
- Requires Heroku CLI and appropriate buildpacks
- See README.md for full deployment instructions
