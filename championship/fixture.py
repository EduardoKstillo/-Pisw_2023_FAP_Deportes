from itertools import combinations
from .models import Team, Game


def generate_fixture(teams_queryset, championship, category):
    teams = list(teams_queryset)

    # si los equipos son impares, agrega o obtiene el equipo DESCANSA
    if len(teams) % 2 != 0:
        teams.append(Team.objects.get_or_create(name="DESCANSA", year='2000')[0])

    fixtures = []
    rounds = len(teams) - 1
    half_size = len(teams) // 2

    for round_number in range(rounds):
        round_fixtures = []
        for i in range(half_size):
            local_team = teams[i]
            print("team local")
            print(local_team)
            away_team = teams[-i - 1]
            print(away_team)
            fixture = Game.objects.create(round_number=round_number + 1, championship=championship,category=category, team1=local_team, team2=away_team)
            round_fixtures.append(fixture)
        fixtures.append(round_fixtures)

        # Rotar equipos en sentido horario, dejando el primer equipo en su lugar
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return fixtures
