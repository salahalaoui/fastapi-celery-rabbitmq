import os

from app.celery_app.tasks import create_task


def test_create_task_text_plain(settings):

    filename = 'file1.txt'
    full_path = str(settings.BASE_DIR / f'tests/data/{filename}')

    output = create_task(full_path, filename, 'text/plain')

    assert output['filename'] == filename
    assert output['result'] == 282

def test_create_task_docx(settings):

    filename = 'example03.docx'
    full_path = str(settings.BASE_DIR / f'tests/data/{filename}')

    output = create_task(full_path, filename, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    assert output['filename'] == filename
    assert output['result'] == 815


