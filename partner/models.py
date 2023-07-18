from django.db import models
from django.contrib.auth.models import User

DEPARTMENT_PERU_CHOICES = [
    ("AM", "Amazonas"),
    ("AN", "Ancash"),
    ("AP", "Apurimac"),
    ("AR", "Arequipa"),
    ("AY", "Ayacucho"),
    ("CA", "Cajamarca"),
    ("CL", "Callao"),
    ("CU", "Cusco"),
    ("HU", "Huancavelica"),
    ("HA", "Huanuco"),
    ("IC", "Ica"),
    ("JU", "Junín"),
    ("LL", "La Libertad"),
    ("LA", "Lambayeque"),
    ("LI", "Lima"),
    ("LO", "Loreto"),
    ("MD", "Madre de Dios"),
    ("MO", "Moquegua"),
    ("PA", "Pasco"),
    ("PI", "Piura"),
    ("PU", "Puno"),
    ("SM", "San Martín"),
    ("TA", "Tacna"),
    ("TU", "Tumbes"),
    ("UC", "Ucayali"),
]


class Partner(models.Model):

    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    num_carnet = models.PositiveIntegerField(
        unique=True, blank=True, null=True)
    date_created = models.DateField(auto_now=True)
    birthdate = models.DateField(null=True, blank=True)
    department = models.CharField(
        max_length=2, choices=DEPARTMENT_PERU_CHOICES, default='Arequipa')
    province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    activity = models.CharField(max_length=100, blank=True, null=True)
    degree_instruction = models.CharField(
        max_length=100, blank=True, null=True)
    civil_status = models.CharField(max_length=100, blank=True, null=True)
    military_card = models.PositiveIntegerField(
        unique=True, blank=True, null=True)
    dni = models.PositiveIntegerField(unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    num_promotion = models.PositiveIntegerField(blank=True, null=True)
    promotion_delegate = models.CharField(
        max_length=100, blank=True, null=True)
    NSA_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
