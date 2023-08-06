import hashlib
import json
import logging
import sys
import time


def init_log(level=logging.DEBUG, filename=None, filemode="w"):
    """

    :param level:
    :param filename: 日志文件路径，默认为None不写文件，
    :param filemode: 可选w覆盖模式,或a添加模式
    """
    logging.basicConfig(level=level,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        filename=filename,
                        filemode=filemode
                        )


def hello():
    print("hello args[%s]" % (sys.argv,))


def world():
    print("world args[%s]" % (sys.argv,))


def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def json_dump(data):
    return json.dumps(data, indent=4)


def print_json(data):
    print(json_dump(data))


def get_timestamp13():
    return str(int(time.time() * 1000))


def get_timestamp10():
    return str(int(time.time()))


def read_file(file_path, mode="r"):
    with open(file_path, mode) as f:
        return f.read()


def save_file(file_path, mode=""):
    with open(file_path, mode) as f:
        return f.write()
