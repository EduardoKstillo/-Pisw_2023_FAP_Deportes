from itertools import combinations
from .models import Team, Game



def generate_fixture(teams_queryset, championship):
    teams = list(teams_queryset)

    if len(teams) % 2 != 0:
        teams.append(Team.objects.get_or_create(name="DESCANSA")[0])

    fixtures = []
    rounds = len(teams) - 1
    half_size = len(teams) // 2

    for round_number in range(rounds):
        round_fixtures = []
        for i in range(half_size):
            local_team = teams[i]
            away_team = teams[-i - 1]
            fixture = Game.objects.create(
                round_number=round_number + 1, championship=championship, team1=local_team, team2=away_team)
            round_fixtures.append(fixture)
        fixtures.append(round_fixtures)

        # Rotar equipos en sentido horario, dejando el primer equipo en su lugar
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return fixtures


def print_fixture(fixtures):
    for idx, round_fixtures in enumerate(fixtures, start=1):
        print(f"Round {idx}:")
        for match in round_fixtures:
            home_team, away_team = match
            home_team = home_team.name if home_team.name != "DESCANSA" else "DESCANSA"
            away_team = away_team.name if away_team.name != "DESCANSA" else "DESCANSA"
            print(f"{home_team} vs {away_team}")
        print()
