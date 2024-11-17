from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Lieu

# Celery tasks
@shared_task
def send_hourly_report():
    """
    Tâche qui envoie un email avec le nombre de lieux ajoutés dans la dernière heure.
    """
    # Calculer la date/heure de la dernière heure
    one_hour_ago = datetime.now() - timedelta(hours=1)
    
    # Compter le nombre de lieux ajoutés dans la dernière heure
    count = Lieu.objects.filter(date_added__gte=one_hour_ago).count()
    
    # Générer le message
    subject = "Rapport horaire des lieux ajoutés"
    message = f"Nombre de lieux ajoutés dans la dernière heure : {count}"
    
    # Envoyer l'email
    send_mail(
        subject,
        message,
        'noreply@example.com',
        ['admin@example.com'],
        fail_silently=False,
    )
    return f"Email envoyé avec {count} lieux ajoutés"
