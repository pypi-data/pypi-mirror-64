"""Auto-generated file, do not edit by hand. AW metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AW = PhoneMetadata(id='AW', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[19]\\d\\d', possible_length=(3,)),
    toll_free=PhoneNumberDesc(national_number_pattern='100|911', example_number='100', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='100|911', example_number='100', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:00|18|76)|91[13]', example_number='100', possible_length=(3,)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='176', example_number='176', possible_length=(3,)),
    sms_services=PhoneNumberDesc(national_number_pattern='176', example_number='176', possible_length=(3,)),
    short_data=True)
