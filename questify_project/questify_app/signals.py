from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Signal untuk membuat profil baru ketika pengguna baru dibuat
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal untuk menyimpan perubahan profil setiap kali pengguna diperbarui
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Menyimpan profil setiap kali data pengguna diperbarui
    if hasattr(instance, 'profile'):
        instance.profile.save()
