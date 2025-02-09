# Task Manager Project

A simple Django-based task management system.

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
python manage.py makemigrations taskmanager
python manage.py migrate
```

4. Create an admin user:
```bash
python manage.py createsuperuser
```

5. Run the server:
```bash
python manage.py runserver
```

## Features
- Project Management
- Task Management
- User Authentication
- Task Categories and Priorities
- Project Team Management
- Task Comments and Updates
