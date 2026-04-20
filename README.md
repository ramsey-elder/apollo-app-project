# Apollo Booking

**CS 3200 — Introduction to Databases | Spring 2026 | Northeastern University**

Apollo Booking is a campus space reservation and facilities management platform. It lets students and student-club representatives find and book rooms, studios, fields, and lecture halls across university buildings; gives administrators full control of users, spaces, bookings, and facility managers; and surfaces booking/usage analytics for data analysts. The application is a three-tier system: a MySQL database, a Flask REST API, and a Streamlit front end — all containerized with Docker.

## Demo and Pitch Video

[Watch the demo and pitch on YouTube](https://youtu.be/k2extcHFPxw)

## Team Members

- Brandon Zau
- Michael Jia
- Nicholas Lee
- Alayna Fu
- Ramsey Elder

## User Personas

Apollo Booking supports four user roles. On the Streamlit landing page, a select widget and "Log In" button for each role mock authentication by loading the chosen user into session state.

| Role | Landing Page | Purpose |
|---|---|---|
| Student | [00_Student_Home.py](app/src/pages/00_Student_Home.py) | Find open spaces, book rooms, file help tickets, manage their own reservations. |
| Club Representative | [10_Club_Rep_Home.py](app/src/pages/10_Club_Rep_Home.py) | Book club-permission spaces, manage club reservations, browse spaces. |
| Administrator | [20_Admin_Home.py](app/src/pages/20_Admin_Home.py) | Manage users, spaces, bookings, and facility managers across the system. |
| Data Analyst | [40_Data_Analyst_Home.py](app/src/pages/40_Data_Analyst_Home.py) | Review booking analytics, building usage, and anomaly reports. |


## Repository Layout

```
apollo-app-project/
├── api/                    # Flask REST API
│   └── backend/            # Blueprints (users, bookings, spaces, buildings,
│                           # clubs, facilities, facility_managers, help_tickets, ...)
├── app/                    # Streamlit front end
│   └── src/pages/          # Role-scoped feature pages
├── database-files/         # DDL + mock data (.sql, executed on container create)
├── datasets/               # Source datasets
├── ml-src/                 # ML model scaffolding
├── docker-compose.yaml     # Service definitions for app, api, db
└── README.md
```

## REST API — Blueprints and Routes

The API is split into eight Blueprints mounted under role- and resource-based URL prefixes in [rest_entry.py](api/backend/rest_entry.py):

| Blueprint | URL Prefix | Resource |
|---|---|---|
| `users` | `/users` | [users_routes.py](api/backend/users/users_routes.py) |
| `bookings` | `/bookings` | [bookings_routes.py](api/backend/bookings/bookings_routes.py) |
| `spaces` | `/spaces` | [spaces_routes.py](api/backend/spaces/spaces_routes.py) |
| `buildings` | `/buildings` | [buildings_routes.py](api/backend/buildings/buildings_routes.py) |
| `clubs` | `/clubs` | [club_routes.py](api/backend/clubs/club_routes.py) |
| `facilities` | `/facilities` | [facilities_routes.py](api/backend/facilities/facilities_routes.py) |
| `facility_managers` | `/facility_managers` | [facility_managers_routes.py](api/backend/facility_managers/facility_managers_routes.py) |
| `help_tickets` | `/help_tickets` | [help_tickets_routes.py](api/backend/help_tickets/help_tickets_routes.py) |

All four HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) are used across the API.

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git (CLI, GitHub Desktop, or the VS Code Git plugin)
- Python 3.11 (only needed locally for IDE autocompletion — the app runs in Docker). [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) is the supported distribution:
  ```bash
  conda create -n db-proj python=3.11
  conda activate db-proj
  pip install -r api/requirements.txt
  pip install -r app/src/requirements.txt
  ```

### 1. Clone the repo

```bash
git clone https://github.com/ramsey-elder/apollo-app-project.git
cd apollo-app-project
```

### 2. Create the `.env` file

The API and database services read secrets from `api/.env`. Copy the template and fill in a password:

```bash
cp api/.env.template api/.env
```

Then open `api/.env` and replace the placeholders:

```
SECRET_KEY=<any-random-string>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=apollo_booking
MYSQL_ROOT_PASSWORD=<choose-a-strong-password>
```

### 3. Start the containers

```bash
docker compose up -d
```

This builds and starts three services:

| Service | Container | Host Port |
|---|---|---|
| Streamlit app | `web-app` | http://localhost:8501 |
| Flask API | `web-api` | http://localhost:4000 |
| MySQL database | `mysql_db` | localhost:3201 |

On the first `up`, MySQL executes every `.sql` file in [database-files/](database-files/) in alphabetical order — the schema in `00_main-ddl.sql` is created first, then mock data for users, buildings, clubs, spaces, bookings, and so on.

Open http://localhost:8501 in your browser and pick a persona to log in as.

### 4. Common Docker commands

```bash
docker compose up -d            # start all services in the background
docker compose stop             # stop without deleting
docker compose down             # stop and remove the containers
docker compose up db -d         # (re)start only the database
docker compose down db -v && docker compose up db -d   # recreate db + re-run .sql files
```
