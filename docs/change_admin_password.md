# Changing Admin Password from Shell

There are two main methods to change the admin password from the shell in this Django application:

## Method 1: Using Django's `changepassword` Management Command

This is the recommended method as it handles all password validation and hashing automatically:

```bash
# Navigate to your project directory
cd /path/to/todo_app

# Run the changepassword command
python manage.py changepassword admin
```

You will be prompted to enter and confirm a new password. The command will validate the password against your configured password validators.

## Method 2: Using Django Shell

If you need to script the password change or can't use the interactive command, you can use the Django shell:

```bash
# Navigate to your project directory
cd /path/to/todo_app

# Start the Django shell
python manage.py shell
```

Then in the Python shell:

```python
# Import the User model
from django.contrib.auth.models import User

# Get the admin user
admin = User.objects.get(username='admin')

# Set the new password
admin.set_password('new_password')

# Save the user object
admin.save()

# Exit the shell
exit()
```

Replace 'new_password' with your desired password.

## Method 3: Using a Custom Management Command

You can also create a one-time script to change the password:

```bash
# Navigate to your project directory
cd /path/to/todo_app

# Run a Python script with Django settings
python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.get(username='admin'); user.set_password('new_password'); user.save(); print('Password updated successfully')"
```

Replace 'new_password' with your desired password.

## Notes

- All methods require you to know the username of the admin account (typically 'admin')
- The password will be hashed according to your Django settings
- After changing the password, you'll need to use the new password to log in