import datetime

from flask import Flask, make_response
from flask import jsonify
from flask import request
from marshmallow import ValidationError

from conf import settings
from exceptions import KeyExistsException, KeyNotExistsException
from models import db
from services import DictionaryService
from validation import DictionaryPostSchema, DictionaryPutSchema, DictionaryDeleteSchema, DictionaryGetSchema, \
    DictionaryPutKeySchema

app = Flask(__name__)

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_ECHO = settings.SQLALCHEMY_ECHO
    SQLALCHEMY_TRACK_MODIFICATIONS = settings.SQLALCHEMY_TRACK_MODIFICATIONS


def initialize_db(app):
    app.app_context().push()
    app.config.from_object(Config)
    db.init_app(app)
    db.init_app(app)
    db.create_all()


@app.route("/dictionary", methods=["POST"])
def set_key():
    """
    Method POST:
     Route: /dictionary
     Запись значения по ключу.
     Команда принимает на вход POST в виде json с параметрами key, value ({"key": "mail.ru", "value": "target"})
     Если ключ уже существует, то 409. Если какой-либо из параметров отсутсвует в запросе, или есть лишние параметры, то 400.

    data = {
         ‘key’: ‘test_key’,
         ‘value’: 'My name is Flask Server',
       }
    :return:
    """
    try:

        data = DictionaryPostSchema().load(request.get_json())
        key = data.get("key")
        value = data.get("value")
        DictionaryService.add_key_value(key=key, value=value)

    except ValidationError as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Invalid parameters provided: {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            400,
        )
    except KeyExistsException:
        return make_response(
            jsonify({"result": "failed", "error": KeyExistsException.message,
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            KeyExistsException.code,
        )
    except Exception as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Unhandled error : {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            500,
        )

    return make_response(
        jsonify({"result": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
        200,
    )


# @app.route('/dictionary/')


@app.route("/dictionary/<key>", methods=["GET"])
def get_key(key):
    """
    Method GET:
     Route: /dictionary/<key>
     Получение значения по ключу.
     Команда принимает на вход один параметр key и отдает значение по ключу из словаря.
     Если ключ не найден, то 404.

    :param key:
    :return:
    """
    try:

        data = DictionaryGetSchema().load({"key": key})
        key, value = DictionaryService.return_key_value(key=data.get("key"))

    except ValidationError as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Invalid parameters provided: {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            400,
        )
    except KeyNotExistsException:
        return make_response(
            jsonify({"result": "failed", "error": KeyNotExistsException.message,
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            KeyNotExistsException.code,
        )
    except Exception as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Unhandled error : {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            500,
        )
    return make_response(
        jsonify(
            {"key": key, "value": value, "result": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
        200,
    )


@app.route("/dictionary/<key>", methods=["PUT"])
def put_key(key):
    """
    Method PUT:
     Route: /dictionary/<key>
     Изменение значения по ключу:
     Запрос аналогичен POST, только если ключ не найден, то 404.

    :param key:
    :return:
    """
    try:
        k = request.get_json()
        data = DictionaryPutSchema().load(request.get_json())
        data_key = DictionaryPutKeySchema().load({"key": key})
        key = data_key.get("key")
        value = data.get("value")
        DictionaryService.overwrite_value(key=key, value=value)

    except ValidationError as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Invalid parameters provided: {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            400,
        )
    except KeyNotExistsException:
        return make_response(
            jsonify({"result": "failed", "error": KeyNotExistsException.message,
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            KeyNotExistsException.code,
        )
    except Exception as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Unhandled error : {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            500,
        )
    return make_response(
        jsonify({"result": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
        200,
    )


@app.route("/dictionary/<key>", methods=["DELETE"])
def delete_key(key):
    """
    Method DELETE:
     Route: /dictionary/<key>
     Удаление значения по ключу.
     Если ключ не найден, то все равно отвечаем 200.

    :param key:
    :return:
    """
    try:
        data = DictionaryDeleteSchema().load({"key": key})
        DictionaryService.delete_value(key=data.get("key"))
    except ValidationError as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Invalid parameters provided: {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            400,
        )
    except KeyNotExistsException:
        return make_response(
            jsonify({"result": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify({"result": "failed", "error": f"Unhandled error : {e.args}",
                     "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
            500,
        )
    return make_response(
        jsonify({"result": "", "time": datetime.datetime.now().strftime("%Y-%m-%d %H.%M")}),
        200,
    )


if __name__ == "__main__":
    initialize_db(app)
    app.run(host="0.0.0.0", port=8000, threaded=True)
