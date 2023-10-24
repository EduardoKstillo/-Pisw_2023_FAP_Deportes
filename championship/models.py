from django.db import models
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

class Player(models.Model):
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#--------------------------
class Person(models.Model):
    name = models.CharField(max_length=30, validators=[validate_str])
    surnames = models.CharField(max_length=30, validators=[validate_str])
    dni = models.PositiveIntegerField(validators=[validate_dni])
    date_created = models.DateTimeField(auto_now_add=True)
    birthdate = models.DateField()
    department = models.IntegerField(
        null=False, blank=False,
        choices=partner_department,
        default=4)
    province = models.CharField(
        max_length=30, blank=False, validators=[validate_str])
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
    address = models.CharField(max_length=50)
    district = models.CharField(max_length=30)
    phone = models.PositiveIntegerField(validators=[validate_phone])
    num_promotion = models.PositiveIntegerField()
    promotion_delegate = models.BooleanField(default=False)
    promotion_sub_delegate = models.BooleanField(default=False)
    partner = models.BooleanField(default=False)
    NSA_code = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='pics', blank=True, null=True)

    def __str__(self):
        return self.name
#-----------------------------

class Team(models.Model):
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=True)
    Persons = models.ManyToManyField(Person)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Championship(models.Model):
    name = models.CharField(max_length=15)
    categorys = models.ManyToManyField(Category) 
    state = models.BooleanField(default=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_finished = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class Game(models.Model):
    round_number = models.PositiveIntegerField(default=0)
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE)
    team1 = models.ForeignKey(
        Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(
        Team, related_name='team2', on_delete=models.CASCADE)
    # date = models.DateTimeField(null=True, blank=True)
    team1_goals = models.IntegerField(default=0)
    team2_goals = models.IntegerField(default=0)
    # state = models.BooleanField(default=True)
    # players = models.ManyToManyField(Player, through="PlayerGame")

    def __str__(self):
        return self.championship.name + " " + self.team1.name + " " + str(self.team1_goals) + "-" + str(self.team2_goals) + " " + self.team2.name

#-----------------------------------


"""
class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card_red = models.IntegerField(default=0)
    card_yellow = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)

    def __str__(self):
        return self.player.name + " " + self.game.championship.name


class Result(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    pj = models.IntegerField(default=0)
    pg = models.IntegerField(default=0)
    pe = models.IntegerField(default=0)
    pp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    # diferencia de goles a favor y en contra
    dg = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)
"""