from django.db import models
from django.contrib.auth.models import User
from .validators import validate_str, validate_dni, validate_phone


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
    name = models.CharField(max_length=30, validators=[validate_str])
    surnames = models.CharField(max_length=30, validators=[validate_str])
    num_carnet = models.PositiveIntegerField(validators=[validate_dni])
    date_created = models.DateTimeField(auto_now_add=True)
    birthdate = models.DateField(blank=True, null=True)
    department = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    province = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    profession = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    activity = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    degree_instruction = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    civil_status = models.CharField(
        max_length=50, blank=True, validators=[validate_str])
    military_card = models.PositiveIntegerField(
        unique=True, null=True, validators=[validate_phone])
    dni = models.PositiveIntegerField(unique=True, validators=[validate_dni])
    address = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=30, blank=True)
    phone = models.PositiveIntegerField(
        blank=True, null=True, validators=[validate_phone])
    num_promotion = models.PositiveIntegerField()
    promotion_delegate = models.BooleanField(default=False)
    NSA_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
