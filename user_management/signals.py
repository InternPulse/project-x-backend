from django.dispatch import Signal

password_reset = Signal(providing_args=["user"])
verification = Signal(providin_args=["user"])