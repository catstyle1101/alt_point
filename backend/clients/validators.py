from django.conf import settings as s
from django.core.exceptions import ValidationError


def passport_series_validator(series: str):
    if len(series) != s.MAX_SERIES_LENGTH:
        raise ValidationError(
            f'Длина серии паспорта должна быть {s.MAX_SERIES_LENGTH}.'
        )
    if not series.isdigit():
        raise ValidationError('Серия паспорта может быть только числом.')


def passport_number_validator(number: str):
    if len(number) != s.MAX_PASSPORT_NUMBER_LENGTH:
        raise ValidationError(
            f'Длина серии паспорта должна быть {s.MAX_PASSPORT_NUMBER_LENGTH}.'
        )
    if not number.isdigit():
        raise ValidationError('Серия паспорта может быть только числом.')


def tin_validator(number: str):
    if not number.isdigit():
        raise ValidationError('ИНН должен состоять из цифр.')
    if len(number) != s.TIN_NUMBER_LENGTH:
        raise ValidationError(f'Длина ИНН должна быть {s.TIN_NUMBER_LENGTH}')
    weights = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
    d1 = str(sum(w * int(n) for w, n in zip(weights, number)) % 11 % 10)
    weights = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
    d2 = str(
        sum(w * int(n) for w, n in zip(weights, number[:10] + d1)) % 11 % 10
    )
    if (d1 + d2) != number[-2:]:
        raise ValidationError('Введен некорректный ИНН.')


def zip_code_validator(zip_code: str):
    if len(zip_code) != 6:
        raise ValidationError('Длина почтового кода неверная')
    if not zip_code.isdigit():
        raise ValidationError('Почтовый код должен состоять только из цифр')
