from flask import jsonify
import datetime
import re


def make_response(msg='success', status_code=200, data=None):
    """
    :param msg: success 成功   fail 失败
    :param status_code: 返回状态码
    :param data: 返回数据
    """
    if data is None:
        data = {}
    response = {
        'msg': msg,
        'status_code': status_code,
        'data': data
    }
    return jsonify(response)


def utc2local(utc_time, ftime='%Y-%m-%d %H:%M:%S'):
    if utc_time:
        time_now = utc_time + datetime.timedelta(hours=8)
        return time_now.strftime(ftime)
    return ''


def get_environs(command) -> dict:
    exp = re.compile(r"-e (\w*?)='?(.*?)'? ")
    env_list = exp.findall(command)
    return {env[0]: env[1] for env in env_list}


def dict2list(env_dict) -> list:
    return [{'key': k, 'value': v} for k, v in env_dict.items()]


def list2dict(env_list) -> dict:
    return {item.get('key'): item.get('value') for item in env_list}
