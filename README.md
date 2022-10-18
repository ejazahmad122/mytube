# MyTube

## Introduction


A social platform like youtube. Where any user can watch videos, only authenticated users can upload videos, comment on the videos, and like or unlink the liked video. Authenticated users will have the facility to view their profiles, change passwords, and reset their passwords via email.


## Installation

Step 1: Setup virtual envrionment
```sh
# create virtual environment
python -m venv django_env
# activate virtual environment
source django_env/bin/activate
```

Step 2: Install requirements
```sh
pip install -r requirements
```

Step 3: Run migrations
```sh
python manage.py migrate
```
Step 4: Run the server
```sh
python manage.py runserver
```


