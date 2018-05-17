from flask import jsonify
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


def parse_sql_error(error):
    """
    解析错误sql返回语句 , 只对IntegrityError有效
    :return 返回元组类型 (code,msg)
    code sql语句中的错误码
    msg  sql语句错误信息
    """
    error = str(error).replace("\\'", '')
    exp = r'(\d+).*"(.*?)"'
    result = re.findall(exp, error)
    if len(result) != 0:
        return result[0]
    return None, None
