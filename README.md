# Spotted Apple :apple::snake:
Spotted Apple allows playlist generation and sharing between Spotify to Apple Music.

## Architecture
The project generally embodies a microservice pattern. The frontend is a Streamlit application, solely providing an interface for the users, and handling some caching for performance. The backend is PostgreSQL instance, with replication/a standby instance.

The backend provides the infrastructure for two containers, one serving as the "primary" server, and the other serving as the "replication" server. While the repository organizes these as such (in directories corresponding to the service they represent) the services constructed are/should be flexible enough to provide high availability without being inherently tied to their founding infrastructure (_i.e., if the primary server fails, the standby server can be promoted, and there's nothing that should either indicate the newly promoted instance was once the standby or hinder it from promotion_).

## TODOs
1. Authenticate with Spotify
2. Authenticate with Google
3. Authenticate with Apple
4. Write Spotify playlists to Google Sheets
