from django.core.management.base import BaseCommand
from reviews.models import Review


class Command(BaseCommand):
    help = "Loads example reviews for the website"

    def handle(self, *args, **kwargs):

        reviews_data = [
            # first_name, last_name, role, role_description, rating, comment
            ("Алексей", "Морозов", "guest", None, 5, "Прекрасная кухня! Французские блюда удивили своим вкусом."),
            ("Мария", "Лебедева", "guest", "Постоянный гость", 5, "Лучшее место в городе. Всегда все на высшем уровне."),
            ("София", "Мартель", "critic", None, 5, "Эталон французской гастрономии."),
            ("Илья", "Константинов", "guest", None, 5, "Очень уютная атмосфера, превосходный сервис."),
            ("Анна", "Рожкова", "other", "Фуд-блогер", 5, "Каждое блюдо — настоящее произведение искусства."),
            ("Жан", "Дюпон", "guest", "Гость из Франции", 5, "Почти как дома! Настоящий вкус Франции."),
            ("Олег", "Стрелков", "guest", None, 5, "Особенно понравилась утка по-бургундски."),
            ("Кристина", "Волкова", "guest", "Постоянный гость", 5, "Всегда свежие продукты и отличный выбор."),
            ("Дмитрий", "Алексеев", "guest", None, 5, "Отлично провели вечер, спасибо!"),
            ("Виктория", "Смирнова", "guest", None, 4, "Хорошо, но хотелось бы чуть быстрее подачу блюд."),
        ]

        self.stdout.write("⏳ Добавляем отзывы...")

        for first, last, role, role_desc, rating, comment in reviews_data:
            Review.objects.create(
                first_name=first,
                last_name=last,
                role=role,
                role_description=role_desc,
                rating=rating,
                comment=comment,
                is_published=True
            )

            self.stdout.write(f"✔ Добавлен отзыв: {first} {last}")

        self.stdout.write(self.style.SUCCESS("Готово! 10 отзывов успешно загружены."))