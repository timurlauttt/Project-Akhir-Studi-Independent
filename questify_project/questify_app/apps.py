from django.apps import AppConfig

class QuestifyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questify_app'

    def ready(self):
        import questify_app.signals  # Pastikan signal diimpor di sini
