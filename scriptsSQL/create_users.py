from django.contrib.auth.models import User, Group
import datetime
import csv

LOGIN = 0
NOMBRE = 1
APELLIDOS = 2
EMAIL = 3
GRUPO = 4

hoy = datetime.datetime.today()

admin, created_admin = Group.objects.get_or_create(name='admin')
secretary, created_secretary = Group.objects.get_or_create(name='secretario')

with open("create_users.csv", "r") as fp:
    reader = csv.reader(fp)
    next(reader)

    for row in reader:
        usuario = User(
            is_superuser=True,
            is_staff=True,
            username=row[LOGIN],
            first_name=row[NOMBRE],
            last_name=row[APELLIDOS],
            email=row[EMAIL],
            is_active=True,
            date_joined=hoy
        )
        usuario.set_password(row[LOGIN])
        usuario.save()
        # asignamos el grupo
        usuario.groups.add(admin if row[GRUPO] == "admin" else secretary)
