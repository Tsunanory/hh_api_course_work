import pytest
from main import key_word_search, user_search
from src.classes import Vacancy

api_call_result = []

vacs = [
        {
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
        },
        {
            "name": "Test Vacancy2",
            "url": "http://example2.com",
            "salary": {
                "from": 21000,
                "to": 22000,
                "currency": "RUR"
            },
            "snippet": {
                "requirement": "Test requirement"
            },
            "experience": {
                "name": "Test experience"
            }
        }
    ]

def testing_user_search(request):
    """Задание ключевого слова для обращения к API, запись результатов в api_call_results"""
    call = vacs
    vacancies = []
    for vac in vacs:
        vacancies.append(Vacancy(vac).__dict__)
    api_call_result.extend(vacancies)
    return vacancies


def test_user_search():
    assert len(testing_user_search("Vacancy")) != 0


def test_key_word_search():
    assert len(key_word_search("Vacancy", vacs)) != 0