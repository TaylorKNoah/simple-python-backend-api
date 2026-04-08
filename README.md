# simple-python-backend-

##### In-Progress

### Purpose
This project showcases my knowledge of building a clean, well built, api in python for business applications.

### Highlights
- OpenAPI / Flask app with Django style project layout ( e.g. models, controllers, repositories, stores, etc )
- Endpoints: Register Account, Login, Logout, SavePreferences
- PostgresSQL DB + Migrations
- JWT Authentication
- Public Hosting + Public Swagger UI via Render
- CI / CD github workflows

### OpenAPI URls
- Local
  - http://localhost:5000/openapi/
  - http://localhost:5000/openapi/swagger#

### To Run ( Host ) Locally
#### Setup virtual env and install packages
Open a terminal and cd into the project directory and run
1. `py -m venv env`
2. start your venv
3. `pip install -r requirements.txt`

#### Setup postgres db
1. [Install postgres](https://www.postgresql.org/download/)
2. Ensure postgre is running.
3. Create db called "simple-python-api-db".
4. In the project, open the .env file and update the DATABASE_URL_DEV to use your password.
5. In a terminal, cd into the project directory and then run the following commands:
    1. `flask db init`
    2. `flask db migrate -m "create users table"`
    3. `flask db upgrade`

### Run the app
1. `py app.py` 

### Tech Stack
| Use | Tech |  
|-----|------|
| Language | Python | 
| Web Framework | Flask |
| .env file & config | python-dotenv |
| Authentication | Flask‑JWT‑Extended |
| Testing | pytest |
| Database  (DB) | PostgreSQL |
| DB Migrations | Alembic + Flask Migrate |
| DB ORM | SQL Alchemy |
| Serialization & Validation | Marshmellow |
| API UI & Documentation |  Swagger|
| Hosting | Render |
