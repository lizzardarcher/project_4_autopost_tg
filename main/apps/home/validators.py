from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import traceback
rus_list = [
    'а', 'б', 'в', 'г', 'д', 'е',
    'ё', 'ж', 'з', 'и', 'й', 'к',
    'м', 'н', 'о', 'п', 'р', 'с',
    'т', 'у', 'ф', 'х', 'ц', 'ч',
    'ш', 'щ', 'ъ', 'ы', 'ь', 'э',
    'ю', 'я', 'л',
]


def validate_non_ascii(value):
    try: str(value).encode('ascii')
    except:
        raise ValidationError(
            _('%(value)s | Имя файла должно содержать только латинские буквы и цифры!'),
            params={'value': value,
                    # 'traceback': traceback.format_exc(),
                    })


def validate_contains_https(value):
    if 'https://t.me/' not in value:
        raise ValidationError(
            _('%(value)s | Поле должно содержать ссылку вида: https://t.me/bla-bla-bla'),
            params={'value': value},
        )


def validate_bot_ref_https(value):
    if 'https://t.me/' not in value:
        raise ValidationError(
            _('%(value)s | Поле должно содержать ссылку вида: https://t.me/mybot'),
            params={'value': value},
        )


def valid_to_upload_excel(value):
    if '.xlsm' not in value or '.xlsx' not in value:
        raise ValidationError(
            _('%(value)s | File must have .xlsm or .xlsx extension'),
            params={'value': value},
        )


def check_code(value):
    if len(str(value).replace(' ', '')) != 16 \
            or ']' in value \
            or '[' in value \
            or '{' in value \
            or '}' in value:
        raise ValidationError(
            _('%(value)s | Code must be consist of 16 symbols, which are only letters and digits'),
            params={'value': value},
        )
