from src.classes import Api_call, Vacancy, JSON_saver
from pprint import pprint

key = 'https://api.hh.ru/vacancies'

to_json = JSON_saver()
api_call_result = []

def user_search(request):
    """Задание ключевого слова для обращения к API, запись результатов в api_call_results"""
    call = Api_call()
    vacancies = []

    for vac in call(key, request)["items"]:
        vacancies.append(Vacancy(vac).__dict__)

    api_call_result.extend(vacancies)


def key_word_search(request):
    """Задаем дополнительное ключевое слово для поиска среди полученных вакансий"""
    vacansies_with_key = []
    for vac in api_call_result:
        for value in vac.values():
            if isinstance(value, str) and request in value:
                vacansies_with_key.append(vac)

    return vacansies_with_key



def user_interaction():
    """Функция взаимодействия с пользователем"""

    cnt = 0
    while not api_call_result:
        if cnt == 0:
            user_request = input("Введите ключевое слово для поиска: ").lower()
            user_search(user_request)
            cnt += 1
        else:
            user_request = input("Мы ничего не нашли по вашему запросу. Задайте новый, например - 'java разработчик': ").lower()
            user_search(user_request)

    to_json(api_call_result, 'data/vacansies.json')
    api_call_result.sort(key=lambda vac: vac["from_sal"] if vac["from_sal"] else vac["to_sal"])

    try:
        user_request = int(input("Далее мы покажем вам вакансии с лучшими зарплатами.\n"
                                 "Введите цифрой количество вакансий, которое вас интересует (по умолчанию покажем 5): "))
        pprint(api_call_result[:-user_request-1:-1])
    except Exception:
        pprint(api_call_result[:-6:-1])


    user_request = 'aaaaaaaaaaaaaaaaaaaaaaa'
    cnt1 = 0
    while not key_word_search(user_request):
        if cnt1 == 0:
            user_request = input(
                "Вы также можете получить список вакансий, которые содержат дополнительное ключевое слово.\n"
                "Введите слово для поиска: ").lower()
            pprint(key_word_search(user_request))
            cnt1 += 1
        else:
            user_request = input(
                "По заданному запросу ничего не нашли.\n"
                "Введите новое слово для поиска: ").lower()
            pprint(key_word_search(user_request))

    return 'Спасибо за использование :)'

print(user_interaction())
