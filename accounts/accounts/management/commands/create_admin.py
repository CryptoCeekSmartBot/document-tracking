from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Change this password after first login!
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User',
                department='Administration',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
            self.stdout.write(self.style.WARNING(f'Default password: {password}'))
            self.stdout.write(self.style.WARNING('IMPORTANT: Change this password immediately after login!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
