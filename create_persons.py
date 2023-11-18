from championship.models import Person
import csv


NOMBRES = 0
APELLIDOS = 1
DNI = 2
REGION = 3
MESPROM = 4
ANOPROM = 5


with open("create_persons.csv", "r") as fp:
    reader = csv.reader(fp)
    next(reader)
    for row in reader:
        persona = Person(
            name=row[NOMBRES],
            surnames=row[APELLIDOS],
            dni=row[DNI],
            department=row[REGION],
            month_promotion=row[MESPROM],
            year_promotion=row[ANOPROM],
        )
        persona.save()
