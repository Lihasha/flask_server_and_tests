from models import Test, db


class DictionaryRepo:
    @staticmethod
    def key_exists(key: str) -> bool:
        return bool(Test.query.filter_by(key=key).first())

    @staticmethod
    def create_key_value(key: str, value: str):
        test_entry = Test(key=key, value=value)
        db.session.add(test_entry)
        db.session.commit()

    @staticmethod
    def return_key_value(key: str):
        value = Test.query.filter_by(key=key).first()
        return key, value.value

    @staticmethod
    def overwrite_value(key: str, value: str):
        test_entry = Test.query.filter_by(key=key).first()
        test_entry.value = value
        db.session.commit()

    @staticmethod
    def delete_value(key: str):
        test_entry = Test.query.filter_by(key=key).first()
        db.session.delete(test_entry)
        db.session.commit()
