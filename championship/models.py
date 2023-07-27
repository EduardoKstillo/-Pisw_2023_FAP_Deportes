from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    state = models.BooleanField(default=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Championship(models.Model):
    name = models.CharField(max_length=15)
    categorys = models.ForeignKey(Category, on_delete=models.CASCADE)
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
