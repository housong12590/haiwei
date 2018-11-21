import re

text = """
docker run -d --name asclepius_api --restart always \
-e ENV_TYPE=Pro \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD='hJYC8PsOsUR45wnDQtGle8cqCFbmN9eY' \
-e MYSQL_HOST='192.168.0.210' \
-e MYSQL_PORT=3306 \
-e MYSQL_DB='asclepius' \
-e REDIS_HOST='192.168.0.210' \
-e REDIS_PASSWORD='' \
-e REDIS_PORT=6379 \
-e HECABA_HOST='http://192.168.0.212:8001' \
-e SMS_HOST='http://192.168.0.212:8011/' \
-e API_VERSION='api/v2/' \
-e LIVE_URL='https://api.lb.jiankanghao.net/api/v1/' \
-e ASCLEPIUS_MGR_IP='http://192.168.0.212:818/' \
-e URL_TO_PDF='http://192.168.0.212:9008/' \
-e PDF_CONFIG='&pdf.margin.top=100&pdf.margin.bottom=100&pdf.printBackground=True' \
-e SECRET_KEY_BASE='37ccc5caf5e7245671aa1d36e4d5f33c6df35082c2ee0557fcf93609ebdc5d9677c29b3a112a995206a933385ad7b0429a32a4bbf90432a4e003617ca3038f5e' \
-p 3005:3000 192.168.0.210/haiwei/asclepius_api
"""
# regexp = re.compile(r"-e (\w*?)='?(.*?)'? ")
# result = regexp.findall(text)
# for i in result:
#     print(i)

text = "registry.jiankanghao.net/haiwei/kx_sms"

try:
    image, tag = text.split(':')
except ValueError:
    image = text
    tag = 'latest'
print(image)
print(tag)
