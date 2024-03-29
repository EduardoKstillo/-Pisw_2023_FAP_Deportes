from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from unidecode import unidecode


def validate_str(value):
    normalized_value = unidecode(value)
    if not re.match(r'^[a-zA-Z ñÑ]+$', normalized_value):
        raise ValidationError(
            'Solo se permiten letras, espacios y la letra \'ñ\' en el texto.')


def validate_dni(value):
    if not (len(str(value)) == 8):
        raise ValidationError(
            _("%(value)s no tiene 8 digitos"),
            params={"value": value},
        )


def validate_phone(value):
    print('telefono :', value)
    if not (len(str(value)) == 9) or len(str(value)) == 0:
        raise ValidationError(
            _("%(value)s no tiene 9 digitos"),
            params={"value": value},
        )

def validate_year(value):
    if not (len(str(value)) == 4):
        raise ValidationError(
            _("%(value)s no tiene 4 digitos"),
            params={"value": value},
        )
    
def validate_month(value):
    if not re.match(r'^[a-zA-Z ]+$', value):
        raise ValidationError(
            'Solo se permiten letras')