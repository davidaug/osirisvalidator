from osiris import _
from osiris.osiris import osiris_validator
from osiris.exceptions import ValidationException
import re


@osiris_validator
def valid_cpf(func, *args, **kwargs):
    message = _('{0} must be valid.'.format(kwargs['field']))
    if 'message' in kwargs:
        message = kwargs['message']

    def wrapper(obj, arg1, arg2):
        if not re.match(r"(^[0-9]+)", arg2):
            raise ValidationException(kwargs['field'], message)

        if len(arg2) < 11:
            raise ValidationException(kwargs['field'], message)

        if arg2 in [s * 11 for s in [str(n) for n in range(10)]]:
            raise ValidationException(kwargs['field'], message)

        calc = [i for i in range(1, 10)]
        d1 = sum([int(a) * (11 - b) for a, b in zip(arg2[:-2], calc)]) % 11
        d1 = 0 if d1 < 2 else (11 - d1)
        calc = [i for i in range(1, 11)]
        d2 = sum([int(a) * (12 - b) for a, b in zip(arg2[:-1], calc)]) % 11
        d2 = 0 if d2 < 2 else (11 - d2)

        if str(d1) != arg2[-2] or str(d2) != arg2[-1]:
            raise ValidationException(kwargs['field'], message)

        return func(obj, arg1, arg2)

    return wrapper
