# Task Manager Project

A comprehensive task and project management system built with Django.

## Features

- Project and Task Management
- Interactive Dashboard
- Team Collaboration
- Task Status Tracking
- Project Analytics
- User Authentication
- Responsive Design

## Tech Stack

- Python 3.8+
- Django 4.0+
- Bootstrap 5
- PostgreSQL
- GitHub Actions

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Deployment

### GitHub Actions Deployment

This project uses GitHub Actions for automated deployment. The workflow:
- Runs tests
- Checks code quality
- Deploys to production when merging to main branch

Prerequisites:
1. Configure GitHub repository secrets:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `ALLOWED_HOSTS`

2. Enable GitHub Pages in repository settings

### Manual Deployment

1. Configure production settings:
```bash
export DJANGO_SETTINGS_MODULE=taskmanager.settings.production
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Run migrations:
```bash
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
