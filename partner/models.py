from django.db import models
from django.contrib.auth.models import User
from .validators import validate_str, validate_dni, validate_phone


partner_department = [
    (1, 'Amazonas'),
    (2, 'Ancash'),
    (3, 'Apurimac'),
    (4, 'Arequipa'),
    (5, 'Ayacucho'),
    (6, 'Cajamarca'),
    (7, 'Callao'),
    (8, 'Cusco'),
    (9, 'Huancavelica'),
    (10, 'Huanuco'),
    (11, 'Ica'),
    (12, 'Junín'),
    (13, 'La Libertad'),
    (14, 'Lambayeque'),
    (15, 'Lima'),
    (16, 'Loreto'),
    (17, 'Madre de Dios'),
    (18, 'Moquegua'),
    (19, 'Pasco'),
    (20, 'Piura'),
    (21, 'Puno'),
    (22, 'San Martín'),
    (23, 'Tacna'),
    (24, 'Tumbes'),
    (25, 'Ucayali'),
]
partner_province=[
    (1, 'Arequipa'),
    (2, 'Camaná'),
    (3, 'Caravelí'),
    (4, 'Castilla'),
    (5, 'Caylloma'),
    (6, 'Condesuyos'),
    (7, 'Islay'),
    (8, 'La Unión'),
]


class Partner(models.Model):

    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, validators=[validate_str])
    surnames = models.CharField(max_length=30, validators=[validate_str])
    num_carnet = models.PositiveIntegerField(validators=[validate_dni])
    date_created = models.DateTimeField(auto_now_add=True)
    birthdate = models.DateField(blank=True, null=True)
    department = models.IntegerField(
        null=False, blank=False,
        choices=partner_department,
        default=4)
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
