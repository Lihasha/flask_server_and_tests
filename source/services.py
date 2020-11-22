from exceptions import KeyExistsException, KeyNotExistsException
from repository import DictionaryRepo


class DictionaryService:
    @staticmethod
    def add_key_value(key: str, value: str):

        if DictionaryRepo.key_exists(key=key):
            raise KeyExistsException

        DictionaryRepo.create_key_value(key=key, value=value)

    @staticmethod
    def return_key_value(key: str):

        if not DictionaryRepo.key_exists(key=key):
            raise KeyNotExistsException

        return DictionaryRepo.return_key_value(key=key)

    @staticmethod
    def overwrite_value(key: str, value: str):

        if not DictionaryRepo.key_exists(key=key):
            raise KeyNotExistsException

        DictionaryRepo.overwrite_value(key=key, value=value)

    @staticmethod
    def delete_value(key: str):
        if not DictionaryRepo.key_exists(key=key):
            return

        DictionaryRepo.delete_value(key=key)
