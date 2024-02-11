from abc import ABC, abstractmethod


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
