# Spotted Apple Backend 
The Spotted Apple backend consists of an authentication server, operations server, and a PostgreSQL database.

The Authentication server is responsible for all authentication and authorization management, while the Operations server handles all business logic. Both servers share a single PostgreSQL instance* for simplicy in intitial development. While both servers are constructed using Flask and gunicorn as a WSGI, and possess almost identical configurations and containerization, each possess their our requirement files, configuration files, settings, environment variables (env files), and Dockerfile. While this increasing the application complexity and development overhead, it allows for greater modularity in foundation design.

_* The single PostgreSQL instance, in production, is a CloudNative PG Cluster_