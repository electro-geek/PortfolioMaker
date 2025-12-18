from django.core.management.base import BaseCommand
from core.models import PortfolioTemplate


class Command(BaseCommand):
    help = 'Initialize portfolio templates in the database'

    def handle(self, *args, **kwargs):
        templates_data = [
            {
                'name': 'Terminal',
                'slug': 'terminal',
                'description': 'Retro hacker terminal with green monospace text and command-line interface aesthetics',
                'is_active': True,
            },
            {
                'name': 'Renaissance',
                'slug': 'renaissance',
                'description': 'Classical art-inspired design with ornate typography and vintage manuscript styling',
                'is_active': True,
            },
            {
                'name': 'Newspaper',
                'slug': 'newspaper',
                'description': 'Classic newspaper layout with multi-column design and bold print journalism aesthetic',
                'is_active': True,
            },
        ]

        for template_data in templates_data:
            template, created = PortfolioTemplate.objects.update_or_create(
                slug=template_data['slug'],
                defaults=template_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Updated template: {template.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nSuccessfully initialized all templates!')
        )
