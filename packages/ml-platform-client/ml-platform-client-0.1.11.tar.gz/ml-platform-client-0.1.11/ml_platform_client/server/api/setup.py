from ..util.field_type import FieldType
from ..validation.validator import StringValidator, NotNullValidator, ObjectValidator

train_arg_setup = {
    'algorithm': FieldType.String,
    'model_path': FieldType.String,
    'data': FieldType.Object,
    'parameters': FieldType.Object,
    'extend': FieldType.Object,
}

train_validate_setup = {
    'algorithm': StringValidator(32),
    'model_path': StringValidator(1024),
    'data': [NotNullValidator(), ObjectValidator()],
    'parameters': [NotNullValidator(), ObjectValidator()],
    'extend': [NotNullValidator(), ObjectValidator()],
}

predict_arg_setup = {
    'features': FieldType.Object,
    'model_id': FieldType.String,
}

predict_validate_setup = {
    'features': ObjectValidator(),
    'model_id': StringValidator(max_len=64),
}

status_arg_setup = {
    'model_id': FieldType.String,
}

status_validate_setup = {
    'model_id': [StringValidator(max_len=32)],
}

load_arg_setup = {
    'model_path': FieldType.String,
    'model_id': FieldType.String,
    'algorithm': FieldType.String,
}

load_validate_setup = {
    'model_id': StringValidator(max_len=32),
    'model_path': StringValidator(max_len=1024),
}

unload_arg_setup = {
    'model_id': FieldType.String,
}

unload_validate_setup = {
    'model_id': StringValidator(max_len=64),
}
