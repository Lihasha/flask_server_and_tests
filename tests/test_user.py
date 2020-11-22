# Тесты написаны  для более пользовательских сценариев:
# пользоватетель делает post потом делает get этих же данных - как пример позитивного сценария пользователя
# к сожалению я не знаю какой подход у вас применяется - атомарность или поведение пользователя
# В данном случае нет отдельного блока на гет,он покрывается тестами из других блоков
# Плюсы данного подхода - можно сократить количество тестовых сценариев и получать более пользовательский сценарий
# Так же можно объединить делит и пост на полноценные сценарии
import random
import string

import pytest
import requests


def generate_random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class TestUserPostRequest:
    '''
    Тесты для POST запросов
    '''

    def test_post_and_get_got_200(self):
        '''
        пользователь послал валидный пост, получили значение через гет
        '''
        key = generate_random_string(20)
        value = generate_random_string(100)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value

    def test_post_got_409(self):
        '''
        пользователь послал валидный пост и потом снова повторил свой запрос - ключ уже есть в бд, можем получить гет
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 409
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value

    @pytest.mark.parametrize("json", [
        {generate_random_string(10): generate_random_string(10), "value": generate_random_string(10)},
        None,
        {"key": generate_random_string(10), generate_random_string(10): generate_random_string(10)},
    ])
    def test_got_400(self, json):
        '''
        пользователь послал неверный пост с неверным ключем key,неверным ключем value и без данных
        '''
        r = requests.post('http://flask_server:8000/dictionary', json=json)
        assert r.status_code == 400

    @pytest.mark.parametrize("json", [
        {"key": generate_random_string(10), "value": generate_random_string(200)},
        {"key": generate_random_string(200), "value": generate_random_string(10)},
    ])
    def test_put_got_200_get_200(self, json):
        '''
        пользователь послал неверный пост с неверным размером key,неверным размером value
        можно объединить с тестом выше основываясь на том что принято в команде
        '''
        r = requests.post('http://flask_server:8000/dictionary', json=json)
        assert r.status_code == 400
        r = requests.get(f'http://flask_server:8000/dictionary/{json["key"]}')
        if len(json["key"]) > 20:
            assert r.status_code == 400
        else:
            assert r.status_code == 404

    @pytest.mark.parametrize("json", [
        {"key": f"{generate_random_string(3)}Ṱ̺̺̕o͞n̝̗͕̟̜̘̦͟", "value": generate_random_string(10)},
        {"key": generate_random_string(10), "value": "(｡◕ ∀ ◕｡)🙈̞̥̱̳̭͉ͅc̬̟h͡a̫̻̯͘o̫̟̖͍̙̝͉s̗̦̲"},
    ])
    def test_naughty_strings_post(self, json):
        '''
        пользователь послал json с стрингами из https://github.com/minimaxir/big-list-of-naughty-strings
        '''
        r = requests.post('http://flask_server:8000/dictionary', json=json)
        assert r.status_code == 200


class TestPutRequest:
    '''
    Тесты для PUT запросов
    '''

    def test_put_got_200_get_200(self):
        '''
        постом положили значение, проапдейтили через пут
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        value2 = generate_random_string(10)
        r = requests.put(f'http://flask_server:8000/dictionary/{key}', json={"value": value2})
        assert r.status_code == 200
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value2

    def test_put_got_404_get_404(self):
        '''
        значения нет в бд, проапдейтили через пут
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.put(f'http://flask_server:8000/dictionary/{key}', json={"value": value})
        assert r.status_code == 404
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 404

    def test_put_got_400_no_data(self):
        '''
        значения есть в бд, послали пут без даты
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        r = requests.put(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 400
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value

    def test_abnormal_big_data(self):
        '''
        значения есть в бд, послали пут с большим значением
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        value2 = generate_random_string(101)
        r = requests.put(f'http://flask_server:8000/dictionary/{key}', json={"value": value2})
        assert r.status_code == 400
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value

    def test_naughty_strings(self):
        '''
        значения есть в бд, послали пут с стрингами из https://github.com/minimaxir/big-list-of-naughty-strings
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.post('http://flask_server:8000/dictionary', json={"key": key, "value": value})
        assert r.status_code == 200
        value2 = "(｡◕ ∀ ◕｡)🙈̞̥̱̳̭͉ͅc̬̟h͡a̫̻̯͘o̫̟̖͍̙̝͉s̗̦̲"
        r = requests.put(f'http://flask_server:8000/dictionary/{key}', json={"value": value2})
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        assert r.json()["key"] == key
        assert r.json()["value"] == value2


class TestDeleteRequest:
    '''
    Тесты для DELETE запросов
    '''

    def test_got_200_existing_key(self):
        '''
        значения есть в бд, удалили,проверили что удалилось
        '''
        key = generate_random_string(10)
        value = generate_random_string(10)
        r = requests.delete(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 404

    def test_got_200_non_existing_key(self):
        '''
        значений нет в бд, удалили,проверили что удалилось
        '''
        key = generate_random_string(10)
        r = requests.delete(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 200
        r = requests.get(f'http://flask_server:8000/dictionary/{key}')
        assert r.status_code == 404
