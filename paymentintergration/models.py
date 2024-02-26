from django.db import models

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment: {self.amount}"
