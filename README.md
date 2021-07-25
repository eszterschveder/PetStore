# Pet Store Tests

Basic tests for Open API's example API, Pet Store, which covers pet's CRUD part.


## Environment Setup

- Create a new virtual environment by executing `python -m venv venv` in a shell
- Activate the environment with `venv/Scripts/activate`
- Install required dependencies by running `pip install -r requirements.txt`


## Running tests

Tests are implemented with **pytest**, so running tests is as easy as running `pytest` in a shell where the virtual environment is activated.


## Further improvements

This implementation contains only the most basic tests.
It should include:
- negative tests (e.g. try to add a new pet with existing id, update pet with invalid id, delete non-existing pet)
- adding pets with different properties
- updating fields other than status
- updating a field multiple times
