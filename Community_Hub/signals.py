from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, User, PostVerification
from django.conf import settings
from twilio_send_otp import send_message

VERIFICATION_THRESHOLD = 2

@receiver(post_save, sender=PostVerification)
def update_post_status_and_notify(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post

    true_count = post.verification.filter(status="true").count()
    false_count = post.verification.filter(status="false").count()

    new_status = post.status
    if true_count >= VERIFICATION_THRESHOLD and true_count > false_count:
        new_status = "verified"
    elif false_count >= VERIFICATION_THRESHOLD and false_count > true_count:
        new_status = "rejected"
    elif true_count + false_count >= VERIFICATION_THRESHOLD and true_count == false_count:
        new_status = "needs_review"

    if post.status != new_status:
        post.status = new_status
        post.save(update_fields=['status'])

    if post.status == "verified" and not post.notified and true_count >= VERIFICATION_THRESHOLD:
        for user in User.objects.all():
            if user.phone_number:
                message_body = (
                    f"Hello {user.first_name}!\n"
                    f"New Information for you:\n"
                    f"Title: {post.title}\n"
                    f"Description: {post.description}\n"
                    f"Location: {post.location}\n"
                    f"Date: {post.event_date}"
                )
                try:
                    send_message(user.phone_number, message_body)
                    print(f"Notification sent to {user.phone_number}")
                except Exception as e:
                    print(f"Failed to send message to {user.phone_number}: {e}")

        post.notified = True
        post.save(update_fields=['notified'])
