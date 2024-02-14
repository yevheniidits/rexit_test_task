from datetime import date

from pydantic import BaseModel
from pydantic import EmailStr


class DatasetRowSerializer(BaseModel):
    category: str
    first_name: str
    last_name: str
    email: EmailStr
    gender: str
    birth_date: date


class ReadCsvResponseFailedRowSerializer(BaseModel):
    row_number: int
    fail_reason: str


class ReadCsvResponseSerializer(BaseModel):
    success: int
    failed: int
    failed_rows: list[ReadCsvResponseFailedRowSerializer]


class FilteredDataRowResponseSerializer(DatasetRowSerializer):
    id: int
