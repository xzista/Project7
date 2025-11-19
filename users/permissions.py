# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
#
# from .models import User
#
#
# def create_groups_and_permissions():
#     # Создаем группы
#     customer_group, created = Group.objects.get_or_create(name='Customers')
#     admin_group, created = Group.objects.get_or_create(name='RestaurantAdmins')
#
#     # Получаем контент-тип для модели User
#     user_content_type = ContentType.objects.get_for_model(User)
#
#     # Получаем или создаем пермишены
#     can_manage_bookings, created = Permission.objects.get_or_create(
#         codename='can_manage_bookings',
#         content_type=user_content_type,
#         defaults={'name': 'Can manage all bookings'}
#     )
#
#     can_view_all_bookings, created = Permission.objects.get_or_create(
#         codename='can_view_all_bookings',
#         content_type=user_content_type,
#         defaults={'name': 'Can view all bookings'}
#     )
#
#     # Назначаем пермишены группам
#     admin_group.permissions.add(can_manage_bookings, can_view_all_bookings)
#     customer_group.permissions.remove(can_manage_bookings, can_view_all_bookings)
#
#     # Сигнал для создания групп при миграциях
#     @receiver(post_migrate)
#     def create_user_groups(sender, **kwargs):
#         if sender.name == 'users':
#             create_groups_and_permissions()
