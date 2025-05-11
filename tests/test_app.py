import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PDF Presentation Converter' in response.data

def test_upload_no_file(client):
    """Test upload endpoint with no file"""
    response = client.post('/upload')
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_process_no_data(client):
    """Test process endpoint with no data"""
    response = client.post('/process')
    assert response.status_code == 400 