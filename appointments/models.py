from django.db import models


class Professional(models.Model):
    social_name = models.CharField(max_length=150)
    profession = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.social_name


class Appointment(models.Model):
    date = models.DateTimeField()
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    def __str__(self):
        return f"{self.professional.social_name} - {self.date}"
