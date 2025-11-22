from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class PhoneNumberValidator(RegexValidator):
    regex = '^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message ='phone number must be a valid 12 digits like 98xxxxxxxxxx'
    code = 'invalid_phone_number'

class SKUValidator(RegexValidator):
    regex = '^[a-zA-Z0-9\-\]{6,20}'
    message = 'sku must be alphanmeric with 6 to 20 characters'
    code = 'invalid_sku'

validate_phone_number = PhoneNumberValidator()
validate_sku = SKUValidator()