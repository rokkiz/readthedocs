import requests, json
import base64

url = "https://api.kontakt.io/device?q=uniqueId==kh9z"
headers = {
"Api-Key": "ndBmmzDbMQrjLCUzPAFdrZldqGFPAHMd",
"Accept": "application/vnd.com.kontakt+json; version=9"
}


configCreateUrl = "https://api.kontakt.io/config/encrypt?uniqueId=2rVo"
response = requests.get(configCreateUrl, headers=headers)
_json =str(json.loads(response.text))
#print(json.dumps(_json, indent=4, sort_keys=True))
_ls = eval(_json)
cf = _ls["configs"]
a = cf[0]["config"]
decoded = base64.b64decode(a)
print([_i for _i in decoded])


