import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task Manager' in response.data

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert 'tasks_count' in json_data

def test_add_task(client):
    """Test adding a new task"""
    response = client.post('/add', data={
        'title': 'Test Task',
        'description': 'This is a test task'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_api_get_tasks(client):
    """Test API endpoint to get all tasks"""
    # Add a task first
    client.post('/add', data={
        'title': 'API Test Task',
        'description': 'Testing API'
    })
    
    # Get tasks via API
    response = client.get('/api/tasks')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_toggle_task(client):
    """Test toggling task completion status"""
    # Add a task
    client.post('/add', data={'title': 'Toggle Test'})
    
    # Toggle it
    response = client.get('/toggle/1', follow_redirects=True)
    assert response.status_code == 200

def test_delete_task(client):
    """Test deleting a task"""
    # Add a task
    client.post('/add', data={'title': 'Delete Test'})
    
    # Delete it
    response = client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200
