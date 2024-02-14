import csv
import tempfile
from datetime import date
from typing import Annotated

from fastapi import UploadFile
from fastapi import Query
from fastapi import File
from fastapi import APIRouter
from starlette.responses import FileResponse

from apps.dataset_processor.db_service import DatasetDbService
from apps.dataset_processor.serializers import DatasetRowSerializer
from apps.dataset_processor.serializers import FilteredDataRowResponseSerializer
from apps.dataset_processor.serializers import ReadCsvResponseFailedRowSerializer
from apps.dataset_processor.serializers import ReadCsvResponseSerializer
from apps.utils import validate_file_type

router = APIRouter(
    prefix='/api',
    tags=['Dataset Processor'],
)


@router.post('/read_csv/')
async def read_csv(file: UploadFile = File(...)) -> ReadCsvResponseSerializer:
    """
    This endpoint reads a CSV file uploaded via a POST request, processes its contents,
    and saves valid rows to a dataset in the database.
    CSV file must contain next columns: category, firstname, lastname, email, gender, birthDate.
    It returns a response indicating the number of successfully processed rows and any rows that failed to be processed.
    """
    validate_file_type(file, ['text/csv'])
    contents = await file.read()
    decoded_contents = contents.decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_contents, delimiter=',')

    total_success_rows = 0
    failed_rows = []

    for row_number, row in enumerate(reader):
        try:
            dataset_row = DatasetRowSerializer(
                category=row['category'],
                first_name=row['firstname'],
                last_name=row['lastname'],
                email=row['email'],
                gender=row['gender'],
                birth_date=row['birthDate'],
            )
            await DatasetDbService().save_dataset_row(dataset_row)
            total_success_rows += 1
        except Exception as err:
            failed_rows.append(ReadCsvResponseFailedRowSerializer(
                row_number=row_number,
                fail_reason=str(err).replace('\n', ' '),
            ))

    return ReadCsvResponseSerializer(
        success=total_success_rows,
        failed=len(failed_rows),
        failed_rows=failed_rows,
    )


@router.get('/filter_data/')
async def filter_data(
        category: str | None = None,
        gender: str | None = None,
        birth_date: date | None = None,
        age: int | None = None,
        age_range: Annotated[
            str | None,
            Query(
                min_length=3,
                max_length=50,
                pattern=r'^(?P<from_age>\d+)-(?P<to_age>\d+)$',
                description='Example: 25-30',
            ),
        ] = None,
) -> list[FilteredDataRowResponseSerializer]:
    """
    This endpoint retrieves data from the dataset in the database based on specified filter criteria.
    It accepts query parameters for filtering by category, gender, birthdate, age, or age range.
    It returns a list of data rows that match the filter criteria.
    """
    filtered_data = await DatasetDbService().filter_data(category, gender, birth_date, age, age_range)
    return filtered_data


@router.get('/csv_export/')
async def filter_data(
        category: str | None = None,
        gender: str | None = None,
        birth_date: date | None = None,
        age: int | None = None,
        age_range: Annotated[
            str | None,
            Query(
                min_length=3,
                max_length=50,
                pattern=r'^(?P<from_age>\d+)-(?P<to_age>\d+)$',
                description='Example: 25-30',
            ),
        ] = None,
) -> FileResponse:
    """
    This endpoint filters data from the dataset in the database based on specified filter criteria
    and exports the filtered data to a CSV file.
    It accepts query parameters for filtering by category, gender, birthdate, age, or age range.
    The exported CSV file contains the filtered data.
    """
    filtered_data = await DatasetDbService().filter_data(category, gender, birth_date, age, age_range)
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=list(filtered_data[0].keys()))
        writer.writeheader()
        writer.writerows(filtered_data)
        return FileResponse(temp_file.name, filename='filtered_dataset.csv')
