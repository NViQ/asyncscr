import os, io
import sys
import hashlib
import pytest
from asynscr import download_repo, calculate_sha256


@pytest.fixture
def temp_folder():
    folder = 'temp_test'
    os.makedirs(folder, exist_ok=True)
    yield folder


@pytest.mark.asyncio
async def test_download_repo(temp_folder):
    url = 'https://gitea.radium.group/radium/project-configuration'
    await download_repo(url, temp_folder)
    assert os.path.isfile(os.path.join(temp_folder, 'repo_content'))


@pytest.mark.asyncio
async def test_calculate_sha256(temp_folder, monkeypatch, capsys):
    file_content = b'Test file.'
    file_name = 'test.txt'
    file_path = os.path.join(temp_folder, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_content)

    # Redirect stdout to a StringIO object to capture the output
    fake_stdout = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', fake_stdout)

    # Call the function and capture the output
    await calculate_sha256(temp_folder)
    output = fake_stdout.getvalue()

    # Restore the original stdout
    monkeypatch.undo()

    file_sha256 = hashlib.sha256(file_content).hexdigest()
    assert f"{file_name}: {file_sha256}" in output

