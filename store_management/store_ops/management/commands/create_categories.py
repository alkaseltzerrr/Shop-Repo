from django.core.management.base import BaseCommand
from store_ops.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories for the store'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and accessories'
            },
            {
                'name': 'Clothing',
                'description': 'Apparel and fashion items'
            },
            {
                'name': 'Books',
                'description': 'Books and publications'
            },
            {
                'name': 'Food & Beverages',
                'description': 'Consumable items'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home decor and gardening items'
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sporting goods and outdoor equipment'
            },
            {
                'name': 'Beauty & Health',
                'description': 'Personal care and health products'
            },
            {
                'name': 'Toys & Games',
                'description': 'Recreational items and games'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_data["name"]}"')
            )
