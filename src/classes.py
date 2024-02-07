from abc import ABC, abstractmethod
import json
import requests


class Headhunter_api(ABC):
    """Абстрактный метод, обязующий потомка определить метод получения вакансий"""
    @abstractmethod
    def get_vacancies(self):
        pass


class Vacancy_json(ABC):
    """Абстрактный метод, обязующий потомка определить метод записи в JSON"""
    @abstractmethod
    def vacancy_to_json(self, vacancy):
        pass


class Api_call(Headhunter_api):
    """Обращение к API с поисковым запросом. Вызываемый класс."""

    def get_vacancies(self, key, request):
        api_call = requests.get(key, {"text": request,
                                "area": "113", "per_page": 100, "page": 1}).json()
        return api_call

    def __call__(self, key, request):
        return self.get_vacancies(key, request)


class Vacancy():
    """Облекание запроса API в предпочтительный формат, приведение валют к рублю"""
    def __init__(self, response):
        self.name = response["name"]
        self.link = response["url"]

        if not response["salary"]:
            self.from_sal = 0
            self.to_sal = 0
            self.currency = "Валюта не указана"
        else:
            self.from_sal = response["salary"]["from"]
            self.to_sal = response["salary"]["to"]
            if response["salary"]["currency"] == "RUR":
                self.currency = "RUR"
            else:
                data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
                data = data['Valute'][response["salary"]["currency"]]
                if self.from_sal:
                    self.from_sal *= data["Value"]
                if self.to_sal:
                    self.to_sal *= data["Value"]


        self.requirement = response["snippet"]["requirement"]
        self.experience_requirements = response["experience"]["name"]


    def __eq__(self, other):
        """Выявление вакансий равных по зарплате"""
        if self.from_sal and other.from_sal:
            return self.from_sal == other.from_sal
        if self.to_sal and other.to_sal:
            return self.to_sal == other.to_sal
        if self.from_sal and not other.from_sal:
            return self.from_sal == other.to_sal
        if not self.from_sal and other.from_sal:
            return self.from_sal == other.to_sal

    def __lt__(self, other):
        """Выявление меньшей по зарплате вакансии"""
        if self.from_sal and other.from_sal:
            return self.from_sal < other.from_sal
        if self.to_sal and other.to_sal:
            return self.to_sal < other.to_sal
        if self.from_sal and not other.from_sal:
            return self.from_sal < other.to_sal
        if not self.from_sal and other.from_sal:
            return self.from_sal < other.to_sal

    def __gt__(self, other):
        """Выявление большей по зарплате вакансии"""
        if self.from_sal and other.from_sal:
            return self.from_sal > other.from_sal
        if self.to_sal and other.to_sal:
            return self.to_sal > other.to_sal
        if self.from_sal and not other.from_sal:
            return self.from_sal > other.to_sal
        if not self.from_sal and other.from_sal:
            return self.from_sal > other.to_sal

    def __str__(self):
        return f'{self.name}, {self.from_sal}-{self.to_sal},{self.experience_requirements}, {self.requirement}, {self.link}'


class JSON_saver(Vacancy_json):
    """Сохранение всех результатов обращения к API в JSON. Вызываемый класс."""
    def vacancy_to_json(self, vacancies, path):
        data = {"items": vacancies}
        with open(path, 'w', encoding='utf-8') as json_file:
            vac1 = json.dumps(data, ensure_ascii=False)
            json_file.write(vac1)


    def __call__(self, vacancies, path):
        return self.vacancy_to_json(vacancies, path)
