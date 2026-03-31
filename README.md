# simple-python-backend-api

### Purpose
This project showcases my knowledge of building a clean, well built, api in python for business applications.  

It will accessible through a frontend swagger page.

### To Run ( Host ) Locally
#### Setup virtual env and install packages
1. `py -m venv env`
2. start your venv
3. `pip install -r requirements.txt`

#### Setup postgres db
1. [install postgres](https://www.postgresql.org/download/)
2. ensure postgre is running
3. create db called "simple-python-api-db"
4. run the following commands
    - `flask db init`
    - `flask db migrate -m "create users table"`
    - `flask db upgrade`

### Run the app
1. `py app.py` 

### Overview
There are 2 api for this project:
1. user login + jwt auth
2. user preferences - using jwt auth

### Tech Stack
| Use | Tech |  
|-----|------|
| Language | Python | 
| Web Framework | Flask |
| Authentication | Flask‑JWT‑Extended |
| Testing | pytest |
| Database  (DB) | PostgreSQL |
| DB Migrations | Alembic |
| DB ORM | SQL Alchemy |
| Serialization & Validation | Marshmellow |
| Flask-Smorest | API framework + Swagger |
| Hosting | Render |