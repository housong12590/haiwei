from models import Project, Image
from app.helper import make_response
import json
import requests


def deploy(url, pid):
    project = Project.find_or_fail(pid)
    image = Image.find_by_tag(project.last_tag)
    if image is None:
        return make_response('还没有绑定镜像', 500)
    data = {
        'id': pid,
        'image': 'registry.jiankanghao.net/{}:{}'.format(image.image_name, image.tag)
    }
    data = json.dumps(data)
    print(url, data)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    resp = requests.post(url, data, headers=headers)
    if resp.status_code == 200:
        return make_response(resp.text)
