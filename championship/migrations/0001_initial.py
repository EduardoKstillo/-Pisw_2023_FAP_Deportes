# Generated by Django 4.2.3 on 2024-01-22 18:37

import championship.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Championship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[championship.validators.validate_str])),
                ('year', models.PositiveIntegerField(validators=[championship.validators.validate_year])),
                ('rule', models.TextField(blank=True, null=True)),
                ('state', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=True)),
                ('categorys', models.ManyToManyField(to='championship.category')),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[championship.validators.validate_str])),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.PositiveIntegerField(default=0)),
                ('team1_goals', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=30)])),
                ('team2_goals', models.PositiveBigIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=30)])),
                ('state', models.BooleanField(default=False)),
                ('sum_team_points', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.category')),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.championship')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[championship.validators.validate_str])),
                ('surnames', models.CharField(max_length=30, validators=[championship.validators.validate_str])),
                ('dni', models.PositiveIntegerField(unique=True, validators=[championship.validators.validate_dni])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('department', models.IntegerField(choices=[(1, 'Amazonas'), (2, 'Ancash'), (3, 'Apurimac'), (4, 'Arequipa'), (5, 'Ayacucho'), (6, 'Cajamarca'), (7, 'Callao'), (8, 'Cusco'), (9, 'Huancavelica'), (10, 'Huanuco'), (11, 'Ica'), (12, 'Junín'), (13, 'La Libertad'), (14, 'Lambayeque'), (15, 'Lima'), (16, 'Loreto'), (17, 'Madre de Dios'), (18, 'Moquegua'), (19, 'Pasco'), (20, 'Piura'), (21, 'Puno'), (22, 'San Martín'), (23, 'Tacna'), (24, 'Tumbes'), (25, 'Ucayali')], default=4)),
                ('province', models.CharField(blank=True, max_length=30)),
                ('district', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('profession', models.CharField(blank=True, max_length=30, validators=[championship.validators.validate_str])),
                ('activity', models.CharField(blank=True, max_length=30, validators=[championship.validators.validate_str])),
                ('degree_instruction', models.CharField(blank=True, max_length=30, validators=[championship.validators.validate_str])),
                ('civil_status', models.CharField(blank=True, max_length=50, validators=[championship.validators.validate_str])),
                ('military_card', models.PositiveIntegerField(blank=True, null=True, unique=True, validators=[championship.validators.validate_phone])),
                ('phone', models.PositiveIntegerField(blank=True, null=True, validators=[championship.validators.validate_phone])),
                ('promotion_delegate', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False)),
                ('promotion_sub_delegate', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False)),
                ('partner', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pics')),
                ('NSA_code', models.CharField(blank=True, max_length=100, null=True)),
                ('month_promotion', models.CharField(max_length=15, validators=[championship.validators.validate_month])),
                ('year_promotion', models.PositiveIntegerField(validators=[championship.validators.validate_year])),
                ('is_jale', models.BooleanField(default=False)),
                ('team_delegate', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[championship.validators.validate_str])),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('month', models.CharField(max_length=100, validators=[championship.validators.validate_month])),
                ('year', models.PositiveIntegerField(validators=[championship.validators.validate_year])),
                ('group', models.CharField(max_length=5)),
                ('state', models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=True)),
                ('persons', models.ManyToManyField(to='championship.person')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pj', models.IntegerField(default=0)),
                ('pg', models.IntegerField(default=0)),
                ('pe', models.IntegerField(default=0)),
                ('pp', models.IntegerField(default=0)),
                ('gf', models.IntegerField(default=0)),
                ('gc', models.IntegerField(default=0)),
                ('dg', models.IntegerField(default=0)),
                ('pts', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.category')),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.championship')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.team')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_red', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=1)])),
                ('card_yellow', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=2)])),
                ('goals', models.PositiveIntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.person')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='championship.PlayerGame', to='championship.person'),
        ),
        migrations.AddField(
            model_name='game',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='championship.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='championship.team'),
        ),
        migrations.CreateModel(
            name='ChampionshipTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.category')),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.championship')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.team')),
            ],
        ),
        migrations.AddField(
            model_name='championship',
            name='disciplines',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.discipline'),
        ),
        migrations.AddField(
            model_name='championship',
            name='seasons',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.season'),
        ),
        migrations.AddField(
            model_name='championship',
            name='teams',
            field=models.ManyToManyField(through='championship.ChampionshipTeam', to='championship.team'),
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='championship.championship')),
            ],
        ),
    ]
