from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def new_robot_notification(sender, instance, created, **kwargs):
    """Уведомление клиентов компании.

    Направление письма(ем) при создании новой записи модели Robots
    с серийным номером, совпадающим с номером в заказе(ах).
    """
    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)

    if orders:
        model = instance.model
        version = instance.version
        for order in orders:
            send_mail(
                subject='новый робот',
                message='Недавно вы интересовались нашим роботом '
                        f'модели {model}, версии {version}. Этот робот теперь '
                        'в наличии. Если вам подходит этот вариант - '
                        'пожалуйста, свяжитесь с нами',
                from_email='orders@r4c.com',
                recipient_list=[order.customer.email, ],
                fail_silently=True,
            )
