import time
import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"
NEW_PET_ID = time.time_ns()


def get_pets_with_status(status='available'):
    return requests.get(f"{BASE_URL}/pet/findByStatus", params={'status': status})


def is_pet_store_updated(pet_id, expected_pets, expected_status_code=200, status='available', retry=20):
    """Check if the expected list of pets present and retry otherwise"""
    if not retry:
        return False
    response = get_pets_with_status(status)
    return (((response.status_code == expected_status_code) and
            (expected_pets == [pet for pet in response.json() if pet['id'] == pet_id])) or
            is_pet_store_updated(pet_id, expected_pets, expected_status_code, status, retry-1))


@pytest.mark.dependency()
def test_get_available_pets():
    """Test whether findByStatus returns a non-empty list of pets when status is available."""
    response = get_pets_with_status()
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)


@pytest.mark.dependency()
def test_add_new_pet():
    """Test if new pet can be added and it's stored."""
    payload = {"id": NEW_PET_ID, "category": {"id": NEW_PET_ID, "name": "string"}, "name": "doggie",
               "photoUrls": ["string"], "tags": [{"id": NEW_PET_ID, "name": "string"}], "status": "available"}
    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    new_pet = response.json()
    assert is_pet_store_updated(NEW_PET_ID, [new_pet], expected_status_code=200, status='available')


@pytest.mark.dependency(depends=["test_add_new_pet"])
def test_update_pet_status():
    """Test if new pet's status can be updated to sold."""
    payload = {"id": NEW_PET_ID, "category": {"id": NEW_PET_ID, "name": "string"}, "name": "doggie",
               "photoUrls": ["string"], "tags": [{"id": NEW_PET_ID, "name": "string"}], "status": "sold"}
    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    updated_pet = response.json()
    assert updated_pet["status"] == "sold"
    assert is_pet_store_updated(NEW_PET_ID, [updated_pet], expected_status_code=200, status='sold')


@pytest.mark.dependency(depends=["test_update_pet_status"])
def test_delete_available_pets():
    """Test whether pet can be deleted successfully."""
    response = requests.delete(f"{BASE_URL}/pet/{NEW_PET_ID}")
    assert response.status_code == 200
    assert NEW_PET_ID == int(response.json()['message'])
    assert is_pet_store_updated(NEW_PET_ID, [], expected_status_code=200, status='sold')
