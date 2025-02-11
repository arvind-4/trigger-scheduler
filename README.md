
# trigger scheduler

A django app that helps with scheduling trigger for a particular period of time.

The Deployed url: https://app-4bk0.onrender.com

## Demo

[![Watch the video](https://raw.githubusercontent.com/arvind-4/trigger-scheduler/refs/heads/main/.github/static/image.png?token=GHSAT0AAAAAAC4TEXJG6OU6WZRAAV2Z7HWMZ5LTC3A)](https://drive.google.com/file/d/1tcwVyYnZySQt05KsZKvrGgdHqwcnQ5FY/view?usp=sharing)


**Demo Video Link:** https://drive.google.com/file/d/1tcwVyYnZySQt05KsZKvrGgdHqwcnQ5FY/view?usp=sharing


## Tech Stack
- Python
- Django
- Bootstrap
- Postgres SQL
- Redis
- Celery

## Run it locally

- Clone the project

```bash
mkdir cd ~/Dev/trigger-scheduler -p
cd ~/Dev/trigger-scheduler
git clone https://github.com/arvind-4/trigger-scheduler.git .
```

- Go to the project directory

```bash
cd ~/Dev/trigger-scheduler
```

If using docker, just run the command to get started

```bash
docker compose up --build
```

Manual Set-up
- Create a virtual environment
- Install dependencies
- Copy the envs
- Set up postgres
- Set up redis
- Set up Celery worker
- Set up Celery Beat
- Run the python server

Copy the `.env.docker` file to `.env`

```bash
python3.10 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
# Run the celery worker
celery -A backend.celery:app worker -l info
# Run the celery beat
celery -A backend.celery:app beat -l info
# Run the python server
python manage.py runserver
```

## Authors

[@Arvind](https://www.github.com/arvind-4)
