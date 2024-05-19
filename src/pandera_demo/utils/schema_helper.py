from typing import Iterable, Type
import pandera as pa


def get_dataset_type_schema(dataset_type: Type[pa.typing.DataFrame]) -> Type[pa.SchemaModel]:
    if not hasattr(dataset_type, '__args__'):
        raise ValueError(f'{dataset_type} is not a generic type')
    type_args = dataset_type.__args__
    if not type_args:
        raise ValueError(f'{dataset_type} has empty args')
    schema_type = dataset_type.__args__[0]
    if not issubclass(schema_type, pa.SchemaModel):
        raise ValueError(f'{dataset_type} is expected to have first type arg of panera.SchemaModel')
    return schema_type


def get_schema_columns(dataset_type: Type[pa.typing.DataFrame]) -> Iterable[str]:
    schema_type = get_dataset_type_schema(dataset_type)
    return schema_type.to_schema().columns.keys()
