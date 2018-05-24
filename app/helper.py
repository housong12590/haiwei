from flask import jsonify


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
