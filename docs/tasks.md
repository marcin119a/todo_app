# Todo App Improvement Tasks

This document contains a prioritized list of tasks to improve the Todo App codebase. Each task is marked with a checkbox that can be checked off when completed.

## Security Improvements

- [x] Move SECRET_KEY to environment variables instead of hardcoding in settings.py
- [x] Configure DEBUG to be False in production environments
- [ ] Set up proper ALLOWED_HOSTS for production
- [ ] Implement proper password reset functionality with secure token handling
- [ ] Add rate limiting for authentication attempts
- [ ] Add validation for file uploads in Profile.avatar to prevent security issues
- [ ] Configure proper CSRF protection for all forms
- [ ] Review and secure email sending functionality

## Architecture Improvements

- [ ] Implement a custom User model instead of extending the default with Profile
- [ ] Reorganize views to be consistently class-based or function-based
- [ ] Move ProjectUpdateView from todo app to project app
- [ ] Set up a proper task scheduling system for reminder emails
- [ ] Configure a production-ready database (PostgreSQL) instead of SQLite
- [ ] Implement proper static files handling for production
- [ ] Set up a caching mechanism for frequently accessed data
- [ ] Create a proper API structure using Django REST Framework

## Code Quality Improvements

- [ ] Remove unused imports (e.g., turtle.update in todo/models.py)
- [ ] Fix duplicate imports (e.g., render, login in todo/views.py)
- [ ] Standardize language usage (currently mixes English and Polish)
- [ ] Add proper docstrings to all models, views, and functions
- [ ] Implement form validation for all user inputs
- [ ] Add error handling for database operations and external services
- [ ] Fix inconsistent URL pattern organization in todo/urls.py
- [ ] Add created_at field to Task model for better tracking
- [ ] Add description field to Task model
- [ ] Remove redundant author field from Comment model (use user instead)
- [ ] Add validation for priority field in Task model (min/max values)
- [ ] Configure email sender address from settings instead of hardcoding

## Testing Improvements

- [ ] Increase test coverage for models
- [ ] Add tests for all views
- [ ] Add tests for forms
- [ ] Add tests for URL routing
- [ ] Add tests for permissions and authentication
- [ ] Improve existing tests for task reminders
- [ ] Add integration tests for the complete workflow
- [ ] Set up CI/CD pipeline for automated testing

## User Experience Improvements

- [ ] Implement better filtering and sorting for tasks
- [ ] Add pagination for task lists
- [ ] Improve mobile responsiveness of templates
- [ ] Add user preferences for email notifications
- [ ] Implement a dashboard with task statistics
- [ ] Add due date reminders in the UI
- [ ] Improve project sharing and collaboration features
- [ ] Add batch operations for tasks (delete multiple, change project, etc.)

## Documentation Improvements

- [ ] Create a comprehensive README.md with setup instructions
- [ ] Document the API endpoints
- [ ] Add inline code comments for complex logic
- [ ] Create user documentation
- [ ] Document the database schema
- [ ] Create developer onboarding guide
- [ ] Document deployment process

## Performance Improvements

- [ ] Optimize database queries in task_list view
- [ ] Implement database indexing for frequently queried fields
- [ ] Set up database connection pooling
- [ ] Implement lazy loading for related objects
- [ ] Configure proper database migrations for production
- [ ] Optimize static files (minification, compression)
- [ ] Implement proper logging for performance monitoring

## Internationalization

- [ ] Set up proper internationalization framework
- [ ] Extract all hardcoded strings to translation files
- [ ] Implement language selection for users
- [ ] Fix mixed language usage (currently has both English and Polish)
- [ ] Add proper date/time formatting for different locales

## Maintenance Tasks

- [ ] Update Django to the latest version
- [ ] Update all dependencies to secure versions
- [ ] Set up dependency scanning for security vulnerabilities
- [ ] Implement proper logging for errors and exceptions
- [ ] Set up monitoring for application health
- [ ] Create backup and restore procedures
- [ ] Implement database migrations strategy
