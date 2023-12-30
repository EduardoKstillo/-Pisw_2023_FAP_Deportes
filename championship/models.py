from django.db import models
from .validators import validate_str, validate_dni, validate_phone, validate_month, validate_year
from django.core.validators import MaxValueValidator


person_department = [
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


BOOLEAN_CHOICES = [
    (False, 'No'),
    (True, 'Si'),
]


class Person(models.Model):
    name = models.CharField(max_length=30, validators=[validate_str])
    surnames = models.CharField(max_length=30, validators=[validate_str])
    dni = models.PositiveIntegerField(unique=True, validators=[validate_dni])
    date_created = models.DateTimeField(auto_now_add=True)
    birthdate = models.DateField(blank=True, null=True)
    department = models.IntegerField(
        null=False, blank=False,
        choices=person_department,
        default=4)
    province = models.CharField(blank=True, max_length=30)
    district = models.CharField(blank=True, max_length=30)
    address = models.CharField(blank=True, max_length=50)
    profession = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    activity = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    degree_instruction = models.CharField(
        max_length=30, blank=True, validators=[validate_str])
    civil_status = models.CharField(
        max_length=50, blank=True, validators=[validate_str])
    military_card = models.PositiveIntegerField(
        unique=True, blank=True, null=True, validators=[validate_phone])
    phone = models.PositiveIntegerField(
        blank=True, null=True, validators=[validate_phone])
    promotion_delegate = models.BooleanField(
        choices=BOOLEAN_CHOICES, default=False)
    promotion_sub_delegate = models.BooleanField(
        choices=BOOLEAN_CHOICES, default=False)
    partner = models.BooleanField(
        choices=BOOLEAN_CHOICES, default=False)
    image = models.ImageField(upload_to='pics', blank=True, null=True)
    NSA_code = models.CharField(max_length=100, blank=True, null=True)
    month_promotion = models.CharField(
        max_length=15, validators=[validate_month])
    year_promotion = models.PositiveIntegerField(validators=[validate_year])
    is_jale = models.BooleanField(default=False)

    def __str__(self):
        return self.name
# -----------------------------


class Team(models.Model):
    name = models.CharField(max_length=50)
    month = models.CharField(max_length=100, validators=[validate_month])
    year = models.PositiveIntegerField(validators=[validate_year])
    group = models.CharField(max_length=5)
    state = models.BooleanField(choices=BOOLEAN_CHOICES, default=True)
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return self.month


class Category(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)

# --Creacion del modelo diciplina


class Discipline(models.Model):
    name = models.CharField(max_length=30, validators=[validate_str])

    def __str__(self):
        return self.name

# --Creacion del modelo temporada


class Season(models.Model):
    name = models.CharField(max_length=30, validators=[validate_str])

    def __str__(self):
        return self.name


class Championship(models.Model):
    name = models.CharField(max_length=20, validators=[validate_str])
    year = models.PositiveIntegerField(validators=[validate_year])
    # --Agregamos los nuevos modelos creados como campos para la creacion de un campeonato
    disciplines = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    seasons = models.ForeignKey(Season, on_delete=models.CASCADE)
    # ----------------------------------------------------------------
    rule = models.TextField(blank=True, null=True)
    categorys = models.ManyToManyField(Category)
    state = models.BooleanField(choices=BOOLEAN_CHOICES, default=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_finished = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team, through='ChampionshipTeam')

    def __str__(self):
        return self.name


class ChampionshipTeam(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.championship.name} - {self.category.name} - {self.team.month}"


class Game(models.Model):
    round_number = models.PositiveIntegerField(default=0)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    team1 = models.ForeignKey(
        Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(
        Team, related_name='team2', on_delete=models.CASCADE)
    # date = models.DateTimeField(null=True, blank=True)
    team1_goals = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(limit_value=30)])
    team2_goals = models.PositiveBigIntegerField(
        default=0, validators=[MaxValueValidator(limit_value=30)])
    # state = models.BooleanField(default=True)
    players = models.ManyToManyField(Person, through="PlayerGame")

    def __str__(self):
        return "Fecha: " + str(self.round_number) + ". " + self.team1.month + " " + str(self.team1_goals) + "-" + str(self.team2_goals) + " " + self.team2.month + " | "

# -----------------------------------


class PlayerGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Person, on_delete=models.CASCADE)
    card_red = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=1)], default = 0)
    card_yellow = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=2)], default = 0)
    goals = models.PositiveIntegerField(default = 0)

    def save(self, *args, **kwargs):
        # Verifica si card_yellow igual a 2
        if self.card_yellow == 2:
            # Si es igual a 2, establece card_red en 1
            self.card_red = 1

        super().save(*args, **kwargs)


class Result(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pj = models.IntegerField(default=0)
    pg = models.IntegerField(default=0)
    pe = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    # diferencia de goles a favor y en contra
    dg = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)
