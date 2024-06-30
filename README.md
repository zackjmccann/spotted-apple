# spotted-apple :apple::snake:
A converter for transferring playlists from Spotify to Apple Music

## Getting Started
1. Copy the `.env-template` file and configure the outlined environment variables.

2. Ensure the Docker daemon is running, then build and run the multi-container application via `docker-compose up`.

3. Provided the build is successful and the containers are running, navigate to the configured URL to to interact with the application (_i.e.,_ `http://[STREAMLIT_HOST]:[STREAMLIT_PORT]`)

## TODOs
1. Authenticate with Spotify
2. Authenticate with Google
3. Write Spotify playlists to Google Sheets
