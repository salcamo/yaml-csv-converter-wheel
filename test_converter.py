import pytest
import requests
from flask import Flask
from app import app

# Create a fixture for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

API_URL = "http://localhost:5000"

def test_yaml_to_csv(client):
    yaml_data = """
---
- id: 1
  name: Johnson, Smith, and Jones Co.
  amount: 345.33
  Remark: Pays on time
- id: 2
  name: Sam "Mad Dog" Smith
  amount: 993.44
  Remark:
- id: 3
  name: Barney & Company
  amount: 0
  Remark: "Great to work with\nand always pays with cash."
- id: 4
  name: 'Johnson''s Automotive'
  amount: 2344
  Remark: 
    """

    headers = {'Content-Type': 'text/yaml'}  # Set the correct content type for YAML
    response = client.post(f"{API_URL}/yaml-to-csv", data=yaml_data.encode('utf-8'), headers=headers)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check the response text for the expected CSV headers
    expected_headers = "id,name,amount,Remark"
    assert expected_headers in response.data.decode('utf-8')

    # Check for the presence of specific expected rows in the CSV
    expected_rows = [
        'id,name,amount,Remark',
        '1,"Johnson, Smith, and Jones Co.",345.33,Pays on time',
        '2,"Sam ""Mad Dog"" Smith",993.44,',
        '3,Barney & Company,0,Great to work with and always pays with cash.',
        '4,Johnson\'s Automotive,2344,',
    ]

    # Check that each expected row is present in the response text
    for row in expected_rows:
        assert row in response.data.decode('utf-8')

    # Optionally, we can also check the total number of rows
    csv_lines = response.data.decode('utf-8').strip().split("\n")
    assert len(csv_lines) == len(expected_rows) # we included the header row but if not, we should add +1

def test_convert_csv_to_yaml(client):
    # Sample CSV data to test the conversion
    csv_data = "name,age,city\nAlice,30,New York\nBob,25,Los Angeles"

    # Send a POST request with CSV data
    response = client.post(
        '/csv-to-yaml',
        data=csv_data,
        content_type='text/csv'
    )

    # Check that the response is 200 OK
    assert response.status_code == 200
    
    # Check that the response is in YAML format
    expected_yaml = "---\n- name: Alice\n  age: 30\n  city: New York\n- name: Bob\n  age: 25\n  city: Los Angeles"
    assert response.data.decode('utf-8') == expected_yaml

def test_invalid_yaml_to_csv(client):
    invalid_yaml = "invalid_yaml_data"
    
    response = client.post(f"{API_URL}/yaml-to-csv", data=invalid_yaml)
    assert response.status_code == 400

def test_invalid_csv_to_yaml(client):
    invalid_csv = "invalid,csv,data"
    
    response = client.post(f"{API_URL}/csv-to-yaml", data=invalid_csv)
    assert response.status_code == 400
