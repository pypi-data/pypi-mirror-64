from drf_yasg.inspectors import SwaggerAutoSchema

from .inspectors import NamedBase64FieldInspector

SwaggerAutoSchema.field_inspectors = [NamedBase64FieldInspector] + SwaggerAutoSchema.field_inspectors
print('drf_base64 __init__.py')
