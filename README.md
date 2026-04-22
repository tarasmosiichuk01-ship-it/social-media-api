# Social Media API

API service for social_media management written on DRF

## Installing using GitHub

```bash
git clone https://github.com/tarasmosiichuk01-ship-it/social-media-api.git
cd social-medai-api
python -m venv venv
source venv/bin/activate  # for MacOS/Linux
venv\Scripts\activate     # for Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Create .env file in root directory with following variables:
```bash
POSTGRES_HOST=<your db hostname>
POSTGRES_DB=<your db name>
POSTGRES_USER=<your db username>
POSTGRES_PASSWORD=<your db user password>
```

## Run with Docker
```bash
git clone https://github.com/tarasmosiichuk01-ship-it/social-media-api.git
cd social-media-api
docker-compose up --build
```

## Getting access

- create user via /api/user/register/
- get access token via /api/user/login/

## Features

- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Managing posts with hashtags, likes and comments
- Filtering posts by authors
- Filtering comments by authors and posts
- Filtering users by username
- Image upload for posts
- Role-based access control (User/Admin)
- Scheduled post creation via Celery
- Follow/unfollow users
- User profile management
