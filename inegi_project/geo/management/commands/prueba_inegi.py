import requests

municipio_id = "03001"
url = f"https://gaia.inegi.org.mx/wscatgeo/mgel/{municipio_id}"
response = requests.get(url, verify=False)
data = response.json()
print(data)
