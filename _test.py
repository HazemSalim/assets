import json
import pytest
from unittest.mock import patch, mock_open  
from fastapi.testclient import TestClient
from processor import EnergyProcessor
from dao import DataAccessor
from controller import app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def sample_data():
    # Define sample data for testing
    data ={
    "asset": [
        {
            "id": 1,
            "name": "High Rise"
        } 
        
    ],
    "asset_energy_demand": [
        {
            "asset": 1,
            "energy_type": 1,
            "energy_demand": 853452
        },
        {
            "asset": 1,
            "energy_type": 2,
            "energy_demand": 724213
        },
        {
            "asset": 1,
            "energy_type": 3,
            "energy_demand": 554321
        },
        {
            "asset": 1,
            "energy_type": 4,
            "energy_demand": 652134
        } 
    ],
    "asset_energy_output": [
        {
            "asset": 1,
            "energy_output": 115432
        } 
    ],
    "energy_system": [
        {
            "id": 1,
            "name": "electricity"
        },
        {
            "id": 2,
            "name": "district_heating"
        },
        {
            "id": 3,
            "name": "coal"
        }
    ],
    "energy_type": [
        {
            "id": 1,
            "name": "heat"
        },
        {
            "id": 2,
            "name": "water"
        },
        {
            "id": 3,
            "name": "light"
        },
        {
            "id": 4,
            "name": "cool"
        }
    ],
    "asset_energy_system": [
        {
            "asset": 1,
            "energy_system": 2,
            "energy_type": 1
        },
        {
            "asset": 1,
            "energy_system": 3,
            "energy_type": 2
        },
        {
            "asset": 1,
            "energy_system": 1,
            "energy_type": 3
        },
        {
            "asset": 1,
            "energy_system": 1,
            "energy_type": 4
        }   
    ]
}

    return json.dumps(data)

def test_get_energy_demand(test_client, sample_data):
    with patch('processor.open', mock_open(read_data=sample_data)):
        response = test_client.get("/energy_demand/1")
        assert response.status_code == 200
        assert response.json() == {
            "name": "High Rise",
            "energy_types": {"heat": 853452, "water": 724213, "light": 438889, "cool": 536702},   
            "total_energy_demand": 2553256,  
            "energy_output_reduction": 8.292171314454833   
        }

def test_get_energy_demand_asset_not_found(test_client, sample_data):
    with patch('processor.open', mock_open(read_data=sample_data)):
        response = test_client.get("/energy_demand/4")
        assert response.status_code == 404
        assert response.json() == {"detail": "Asset not found"}

