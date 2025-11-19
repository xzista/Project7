from django.core.management.base import BaseCommand
from bookings.models import RestaurantTable
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Seed initial tables and create RestaurantAdmins group"

    def handle(self, *args, **options):
        # Создать группу RestaurantAdmins
        group, created = Group.objects.get_or_create(name='RestaurantAdmins')
        if created:
            self.stdout.write("Создана группа RestaurantAdmins")

        # Пример таблиц зала
        # Зал: 8 столиков по 2 места, 4 по 4, 4 по 6, 2 по 8
        counter = 1
        for _ in range(8):
            RestaurantTable.objects.get_or_create(name=f"Hall-2-{counter}", defaults={"table_type":"2-seater", "capacity":2, "location":"hall"})
            counter += 1
        for i in range(1,5):
            RestaurantTable.objects.get_or_create(name=f"Hall-4-{i}", defaults={"table_type":"4-seater", "capacity":4, "location":"hall"})
        for i in range(1,5):
            RestaurantTable.objects.get_or_create(name=f"Hall-6-{i}", defaults={"table_type":"6-seater", "capacity":6, "location":"hall"})
        for i in range(1,3):
            RestaurantTable.objects.get_or_create(name=f"Hall-8-{i}", defaults={"table_type":"8-seater", "capacity":8, "location":"hall"})

        # Терраса: 5 по 2, 5 по 4
        for i in range(1,6):
            RestaurantTable.objects.get_or_create(name=f"Terrace-2-{i}", defaults={"table_type":"2-seater", "capacity":2, "location":"terrace"})
        for i in range(1,6):
            RestaurantTable.objects.get_or_create(name=f"Terrace-4-{i}", defaults={"table_type":"4-seater", "capacity":4, "location":"terrace"})

        self.stdout.write(self.style.SUCCESS("Seed completed."))