from django.core.exceptions import ValidationError

def int_validators(value): 
    if value.isdigit()==False:
        raise ValidationError('ID harus bernilai numerik')