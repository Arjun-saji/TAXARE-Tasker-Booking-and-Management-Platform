from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomerProfile
from .models import Booking, Notification
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model




# User = get_user_model()
def notify_user(user, message):
    """Create a notification for the user."""
    Notification.objects.create(recipient=user, message=message)

def notify_tasker(tasker, message):
    """Create a notification for the tasker."""
    Notification.objects.create(recipient=tasker.user, message=message)

@receiver(post_save, sender=Booking)
def create_booking_notification(sender, instance, created, **kwargs):
    if created:  # Check if the Booking instance was created
        print("Booking created, sending notifications.")
        
        # Ensure we have the correct instance types
        print(f"Type of tasker: {type(instance.tasker)}")  # Should show TaskerProfile
        print(f"Type of customer: {type(instance.customer)}")  # Should show CustomerProfile
        
        # Notify user and tasker about the booking
        customer_message = f"You have booked {instance.tasker.user.username} for {instance.service.name}"
        notify_user(instance.customer.user, customer_message)  # Ensure this is a User instance

        tasker_message = f"You have a booking request from {instance.customer.user.username} for {instance.service.name}"
        notify_tasker(instance.tasker, tasker_message)  # Ensure this is a TaskerProfile instance

          # Create notifications
        Notification.objects.create(
            recipient=instance.customer.user,  # Customer's user
            message=customer_message,
            booking=instance  # Attach the booking instance
        )

        Notification.objects.create(
            recipient=instance.tasker.user,  # Tasker's user
            message=tasker_message,
            booking=instance  # Attach the booking instance
        )


        print("notifications created and it will work ")


