from django.utils import timezone
from .models import Task
from django.core.mail import send_mail

def send_task_reminder_email(task):
    """
    Send an email reminder for a task.
    :param task: Task object to send the reminder for.
    """
    if not task.due_date:
        return  # No due date set, no reminder needed
    subject = f"Przypomnienie: zadanie '{task.title}'"
    message = f"Cześć!\n\nPrzypominamy, że zadanie \"{task.title}\" ma termin wykonania o {task.due_date.strftime('%Y-%m-%d %H:%M')}.\n\nOpis: {task or 'brak opisu'}"
    recipient = task.user.email
    if recipient:
        send_mail(
            subject,
            message,
            'noreply@twojaaplikacja.pl',
            [recipient],
            fail_silently=False
        )

def send_task_reminders():
    """
    Send reminders for tasks that are due within the next hour.
    This function should be scheduled to run periodically.
    """
    now = timezone.now()
    one_hour_later = now + timezone.timedelta(hours=1)
    tasks = Task.objects.filter(
        due_date__gte=one_hour_later,
        due_date__lt=one_hour_later + timezone.timedelta(minutes=1),
        completed=False
    )
    for task in tasks:
        send_task_reminder_email(task)