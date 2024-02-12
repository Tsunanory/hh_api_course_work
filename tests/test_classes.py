import pytest
from src.classes import Vacancy, Api_call
key = 'https://api.hh.ru/vacancies'

@pytest.fixture
def test_Api_call():
    return Api_call()

@pytest.fixture
def vacancy_response():
    return {
        "name": "Test Vacancy",
        "url": "http://example.com",
        "salary": {
            "from": 1000,
            "to": 2000,
            "currency": "RUR"
        },
        "snippet": {
            "requirement": "Test requirement"
        },
        "experience": {
            "name": "Test experience"
        }
    }

@pytest.fixture
def vacancy(vacancy_response):
    return Vacancy(vacancy_response)


def test_eq(vacancy, vacancy_response):
    same_vacancy = Vacancy(vacancy_response)
    assert vacancy == same_vacancy

    same_vacancy.from_sal = 2000
    assert vacancy != same_vacancy


def test_lt(vacancy, vacancy_response):
    same_vacancy = Vacancy(vacancy_response)
    same_vacancy.from_sal = 100
    assert same_vacancy < vacancy


def test_gt(vacancy, vacancy_response):
    same_vacancy = Vacancy(vacancy_response)
    same_vacancy.from_sal = 3000
    assert same_vacancy > vacancy


def test_str(vacancy):
    assert str(vacancy) == 'Test Vacancy, 1000-2000,Test experience, Test requirement, http://example.com'

