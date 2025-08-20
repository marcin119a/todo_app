import os
from todo_app.settings import DEBUG, ALLOWED_HOSTS

# Print the current DEBUG and ALLOWED_HOSTS settings
print(f"Current DEBUG setting: {DEBUG}")
print(f"Current ALLOWED_HOSTS setting: {ALLOWED_HOSTS}")

# Test with DJANGO_DEBUG explicitly set to 'true'
os.environ['DJANGO_DEBUG'] = 'true'
# We need to reload the settings module to see the effect
import importlib
import todo_app.settings
importlib.reload(todo_app.settings)
print(f"DEBUG with DJANGO_DEBUG='true': {todo_app.settings.DEBUG}")
print(f"ALLOWED_HOSTS: {todo_app.settings.ALLOWED_HOSTS}")

# Test with DJANGO_DEBUG explicitly set to 'false'
os.environ['DJANGO_DEBUG'] = 'false'
importlib.reload(todo_app.settings)
print(f"DEBUG with DJANGO_DEBUG='false': {todo_app.settings.DEBUG}")
print(f"ALLOWED_HOSTS: {todo_app.settings.ALLOWED_HOSTS}")

# Test with DJANGO_DEBUG unset (using default)
os.environ.pop('DJANGO_DEBUG', None)
importlib.reload(todo_app.settings)
print(f"DEBUG with DJANGO_DEBUG unset (default): {todo_app.settings.DEBUG}")
print(f"ALLOWED_HOSTS: {todo_app.settings.ALLOWED_HOSTS}")
