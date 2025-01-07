# Spotted Apple :apple::snake:
Spotted Apple allows playlist generation and sharing between Spotify to Apple Music.

### :loudspeaker: 🚧 This repository is actively being developed as a portfolio piece for it's author, [Zachary J. McCann](mailto:zackjmccann@gmail.com) 🚧 :loudspeaker:

## Architecture
### Frontend

The frontend is built Next.js, using the Page Router. The objective is to keep as much application code for user management, Spotify and Apple music API calls, etc., in the backend, and respect the frontend solely as a client. This makes the frontend modular and offloads much of the application logic to the backend. 

The frontend structured as follows (`frontend/spotted-apple/`):

`app`
* Houses all `page.tsx` files and URL paths. These all are client components, and the directory should simply be used to organize the application's pages and paths, and should not house server components or logic

`data-access`
* Houses all functions communicating with backend servers. Components can import these functions, but all backend/outside API calls should be facilitated through functions within this directory

`features`
* All logic required for a page or client component is organized into "features" within this directory. Features should not import any components, objects, types, etc. from other features, and instead should use the `data-access` and `lib` directories. This ensures any code within a features directory is isolated to that feature.

`lib`
* General pupose library for storing application-wide abstractions and reuseable components.

### Backend

The backend is currently comprised of two services: An authentication service and an operations service. Both are servers constructed using `Flask` as the web sever framework, and `gunicorn` as the WSGI. The Authentication service is entirely and solely responsible for authentication and authorization. This sevices provides an API for client authentication (for session management) and user authentication (for application data access). Ideally, this service only interacts with other Spotted-Apple services (_e.g., the operations service_), and clients do not directly interact with this service. The operations service is responsible for interfacing with clients. It fields requests, serving as proxy with the authentication service, and providing the API for application data (profiles, settings, etc.)

All backend services currently share a common PostgreSQL database, where role-base permissions will aim to seperate concerns and data. Once host on GKE, PostgreSQL instances will be managed via [CloudNative PG](https://github.com/cloudnative-pg/cloudnative-pg).

#### _I'm still learning and not entirely a software engineer. The architecture above was chosen to explore some key components to a full stack web application, develop some skills, and learn along the way. The repository has already changed a handful of times since I was originally asked "can you write a script to transfer my playlist for me" and has gotten completely blown out of proportion by developing it into an application._
