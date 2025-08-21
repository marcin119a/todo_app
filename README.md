# Todo App - Django Task Management System

A comprehensive Django-based task management application with user authentication, project organization, task comments, and REST API support.

## 🚀 Features

### Core Functionality
- **Task Management**: Create, edit, delete, and complete tasks
- **Project Organization**: Group tasks by projects with team collaboration
- **User Authentication**: Secure login/registration system with password management
- **Task Comments**: Add, edit, and delete comments on tasks via API
- **Priority System**: Set task priorities (1-5 scale)
- **Due Dates**: Schedule tasks with due dates
- **Tags**: Categorize tasks with custom tags
- **User Profiles**: Customizable user profiles with avatar upload

### Technical Features
- **REST API**: Full API support for comments and task management
- **Responsive Design**: Modern, mobile-friendly interface
- **File Upload**: Avatar image upload functionality
- **Search & Filter**: Find tasks by various criteria
- **Calendar View**: Visual task scheduling interface

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **API**: Django REST Framework
- **Testing**: pytest + pytest-django
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo_app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
todo_app/
├── todo/                    # Main task management app
│   ├── models.py           # Task and Tag models
│   ├── views.py            # Task views and logic
│   ├── urls.py             # Task URL patterns
│   └── templates/todo/     # Task templates
├── project/                # Project management app
│   ├── models.py           # Project model
│   ├── views.py            # Project views
│   └── templates/project/  # Project templates
├── comments/               # Comment system app
│   ├── models.py           # Comment model
│   ├── views.py            # Comment API views
│   ├── serializers.py      # DRF serializers
│   └── tests/              # Comment API tests
├── user/                   # User management app
│   ├── models.py           # User profile model
│   ├── views.py            # User views
│   └── templates/user/     # User templates
├── todo_app/               # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
├── pytest.ini             # pytest configuration
└── manage.py              # Django management script
```

## 🗄️ Database Models

### Task Model
- `user`: Owner of the task
- `project`: Associated project (optional)
- `title`: Task title
- `completed`: Completion status
- `due_date`: Task deadline
- `priority`: Priority level (1-5)
- `tags`: Associated tags
- `updated_at`: Last modification timestamp

### Project Model
- `user`: Project owner
- `name`: Project name
- `description`: Project description
- `members`: Team members (many-to-many)

### Comment Model
- `user`: Comment author
- `task`: Associated task
- `content`: Comment text
- `created_at`: Creation timestamp
- `author`: Author name (fallback)

### Profile Model
- `user`: Associated Django user
- `avatar`: User profile picture

## 🔌 API Endpoints

### Comments API
- `POST /comments/api/add/` - Add new comment
- `PUT /comments/api/edit/<id>/` - Edit comment
- `DELETE /comments/api/delete/<id>/` - Delete comment

### Tasks API
- `GET /todo/api/tags/` - Get available tags

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific app tests
pytest comments/tests/
pytest todo/tests/
pytest user/tests/

# Run with coverage
pytest --cov=todo_app
```

## 🚀 Usage

### Basic Task Management
1. **Register/Login**: Create an account or log in
2. **Create Tasks**: Add new tasks with title, description, and due date
3. **Organize**: Group tasks by projects and add tags
4. **Track Progress**: Mark tasks as complete
5. **Collaborate**: Add team members to projects

### Advanced Features
- **Comments**: Add contextual comments to tasks via API
- **Priority Management**: Set and filter by task priority
- **Calendar View**: Visualize tasks in calendar format
- **Profile Management**: Upload avatars and manage account settings

## 🔒 Security Features

- CSRF protection enabled
- User authentication required for sensitive operations
- Secure file upload handling
- Password validation and hashing
- Session management

## 🎨 Customization

### Adding New Features
1. Create new Django app: `python manage.py startapp new_feature`
2. Add to `INSTALLED_APPS` in settings.py
3. Create models, views, and templates
4. Update URL patterns

### Styling
- Templates use Bootstrap for responsive design
- Custom CSS can be added to static files
- Avatar uploads stored in `media/avatars/`

## 📝 Environment Variables

For production deployment, set these environment variables:
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the Django documentation
- Review the test files for usage examples

## 🔄 Version History

- **v1.0.0**: Initial release with basic task management
- **v1.1.0**: Added project organization and team collaboration
- **v1.2.0**: Implemented comment system with REST API
- **v1.3.0**: Enhanced user profiles and avatar uploads

---

**Happy Task Management! 🎯**
