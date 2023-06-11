import os

import django
import requests
from django.core.management.base import BaseCommand
from google_images_search import GoogleImagesSearch

from menu.models import Category, Dish


def create_categories_and_dishes():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_delivery.settings.development')
    django.setup()

    categories_data = {
        'Desserts': [
            ('Chocolate cake', 7.99, 'Rich, moist chocolate cake topped with chocolate frosting.', False, False),
            ('Cheesecake', 6.99, 'Creamy, tangy cheesecake with a graham cracker crust.', True, False),
            ('Tiramisu', 8.99, 'Layered dessert made with espresso-soaked ladyfingers and creamy mascarpone cheese.', True, False),
            ('Ice cream sundae', 4.99,
             'Vanilla ice cream topped with hot fudge, whipped cream, and a cherry.', True, True),
            ('Apple pie', 5.99, 'Classic apple pie with a flaky crust and warm, cinnamon-spiced filling.', True, False),
        ],
        'Drinks': [
            ('Margarita', 7.99, 'Classic cocktail made with tequila, lime juice, and triple sec. Served on the rocks with a salt rim.', True, True),
            ('Mojito', 8.99, 'Refreshing cocktail made with rum, lime juice, sugar, mint leaves, and soda water.', True, True),
            ('Cosmopolitan', 7.99, 'Sweet and tart cocktail made with vodka, triple sec, cranberry juice, and lime juice.', True, True),
            ('Old Fashioned', 10.99, 'Classic cocktail made with whiskey, bitters, sugar, and a twist of orange. Served on the rocks.', True, True),
            ('Espresso martini', 9.99,
             'Bold cocktail made with vodka, espresso, coffee liqueur, and a touch of sugar.', True, True),
        ],
        'Pizzas': [
            ('Margherita pizza', 12.99,
             'Classic pizza with tomato sauce, fresh mozzarella, and basil.', True, False),
            ('Pepperoni pizza', 14.99,
             'Pizza with tomato sauce, mozzarella cheese, and spicy pepperoni slices.', False, False),
            ('Hawaiian pizza', 13.99,
             'Pizza with tomato sauce, mozzarella cheese, ham, and pineapple.', False, False),
            ('Meat lover\'s pizza', 16.99,
             'Pizza with tomato sauce, mozzarella cheese, pepperoni, sausage, bacon, and ham.', False, False),
            ('BBQ chicken pizza', 14.99,
             'Pizza with BBQ sauce, mozzarella cheese, chicken, red onions, and cilantro.', False, False),
        ],
        'Pastas': [
            ('Fettuccine Alfredo', 13.99,
             'Rich and creamy dish with fettuccine noodles and a buttery parmesan sauce.', True, False),
            ('Lasagna', 14.99, 'Layered dish with lasagna noodles, meat sauce, and ricotta cheese.', False, False),
            ('Pesto pasta', 13.99, 'Dish with spaghetti noodles tossed in a vibrant green pesto sauce made with basil, garlic, and pine nuts.', True, False),
            ('Carbonara', 14.99, 'Classic dish with spaghetti noodles, bacon, egg yolks, and parmesan cheese.', False, False),
            ('Marinara with shrimp or chicken', 15.99,
             'Dish with spaghetti noodles and a tomato-based sauce with your choice of shrimp or chicken.', False, False),
        ],
        'Starters': [
            ('Bruschetta', 6.99, 'Toasted bread with a mixture of tomatoes, garlic, basil, and olive oil.', True, False),
            ('Fried calamari', 9.99, 'Crispy and tender calamari rings served with marinara sauce.', False, False),
            ('Spinach and artichoke dip', 7.99,
             'Creamy dip made with spinach, artichokes, and melted cheese. Served with tortilla chips.', True, True),
            ('Buffalo wings', 9.99, 'Spicy chicken wings served with a side of blue cheese dressing.', False, True),
            ('Onion rings', 6.99, 'Crispy battered onion rings served with ranch dressing.', True, False),
        ],
        'Mains': [
            ('Grilled steak', 19.99, 'Juicy and flavorful steak cooked to your preference and served with a side of vegetables and mashed potatoes.', False, True),
            ('Roasted chicken', 14.99,
             'Tender and juicy roasted chicken served with a side of roasted vegetables and rice.', False, True),
            ('Grilled salmon', 16.99,
             'Fresh salmon fillet grilled to perfection and served with a side of quinoa and vegetables.', False, True),
            ('Chicken Parmesan', 15.99, 'Breaded chicken breast topped with tomato sauce and melted mozzarella cheese, served with a side of spaghetti.', False, False),
            ('Veggie stir fry', 12.99,
             'Fresh vegetables stir-fried with a choice of tofu or mixed nuts, served with a side of rice.', True, True),
        ],
    }

    image_dir = 'restaurant_delivery/media'

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    for category_name, dishes in categories_data.items():
        category_image_path = os.path.join(
            'categories', f"{category_name.replace(' ', '_').lower()}.jpg")

        # download_image(category_name, category_image_path)

        category, _ = Category.objects.get_or_create(name=category_name, image=category_image_path)
        for dish in dishes:
            dish_name, price, description, is_vegetarian, is_gluten_free = dish
            dish_image_path = os.path.join('dishes', f"{dish_name.replace(' ', '_').lower()}.jpg")

            # download_image(dish_name, dish_image_path)

            Dish.objects.get_or_create(
                name=dish_name,
                price=price,
                description=description,
                image=dish_image_path,
                is_vegetarian=is_vegetarian,
                is_gluten_free=is_gluten_free,
                category=category,
            )


class Command(BaseCommand):
    help = 'Populates the database with initial data.'

    def handle(self, *args, **options):
        create_categories_and_dishes()
        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))
