
import time
from celery import shared_task

from app.config import settings
from app.TextAnalysis import analysis

@shared_task(name="create_task")
def create_task(file_location, original_filename, mime_type):

    text = settings.ACCEPTED_FILE_TYPES[mime_type](file_location, original_filename).extract_text()
    output = analysis.text_analysis(text)

    return {
        'result': output,
        'filename': original_filename
    }


