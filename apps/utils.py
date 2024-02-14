from fastapi import UploadFile, HTTPException
from starlette import status


def validate_file_type(file: UploadFile, accepted_file_types: list[str]):
    if file.content_type not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='Unsupported file type',
        )
