import requests
from requests.cookies import RequestsCookieJar

url = "https://c0.avaamo.com/"

headers = {
    'authority': "c0.avaamo.com",
    'cache-control': "max-age=0,no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'referer': "https://c0.avaamo.com/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9",
#    'cookie': "timezone=America/Los_Angeles; _ga=GA1.2.158832917.1542741906; hubspotutk=17c9a013336f114ae166002501d5e62a; __hstc=38728700.17c9a013336f114ae166002501d5e62a.1542814023881.1543429241108.1543449352891.3; __adroll_fpc=41a6089814f3f2d1f634179c183a67fc; __idcontext=eyJjb29raWVJRCI6IlRaM0REUFJNM0xDVEJUNE1JVEtQWlAyTkRJU1hIN080SUlRM05HRUg0TUpRPT09PSIsImRldmljZUlEIjoiVFozRERQUk0zSFlRM1U2SU42S0tYS1NDRkYySEgzT0hJSUJNQk1VTDJRUFE9PT09IiwiaXYiOiJKUlhNVkJXUzJFRjdOUVhRNlVaTUkyQVdMTT09PT09PSIsInYiOjF9; __ar_v4=G5MAO3I2MZF5DIYRUN4FZG%3A20181128%3A11%7CSVDU36K6YBCX3GITNQXKGO%3A20181128%3A11%7CHHFOBWL63ZBLNERWK4N55S%3A20181128%3A11; _fbp=fb.1.1549470607441.1258546098; __utmz=231280079.1550008087.12.3.utmcsr=c0.avaamo.com|utmccn=(referral)|utmcmd=referral|utmcct=/web_channels/fe202ece-6afc-470e-a46d-ae5065bc5f3d/channel; __utma=231280079.158832917.1542741906.1550008087.1550061017.13; remember_dashboard_user_token=W1s0ODddLCJ4Z2lFNVplcHhzdjk1MlZISER4dyIsIjE1NTE4NDMyMjEuNDUyODYwOCJd--651c46768934aec5a840d483cb1eeb0ed814d6d7; _gid=GA1.2.364691170.1551995603; _dashboard_session=eWt6aW1BVy9na3JVdTBQRStFOFZadjQ1Y215T3NFUHhOa2pHLzNUK3FxbjdiaXFFajFCRkJNSHdzcDF4WnM2TW1Gbi9ZYzMzM2NRZjRVU3lVYWtMeS9yMXNoZEtmL1Rmc1k2bTNSTjdyUFJNWHI5a0Q5L3pweUR4WldQcDduRERpdmxLSmZLYmxENU5wWXM3aCtRK25ZR0V1RHU3ZWpSVGU2T3h4MWlOY3lXaTF1QnRGeXlrVy9tTTdnczIyVUk3TG9teXVRS1JhSDAxOWhneVVBOEpVaFNCY041T2RhcnpjRDBXZ3RyUXBoVkpSU1ZtckxoVGczcEc5NWZiMjJxQXNXb1NOcVN4clAzVjdiKzZmaEpIcFE0TWFiSk9wa0d5bWpoMUxyeDdia1hGUmIwRGdXMXNVZFF2cW5aYkJpVUE3dFZMUGk3YUFTZnAxNFZxc3Vub3NjV0sxR0RpNFZvbFlUWGNxQ1pEUDVPTjdNalh2dlBXNVBXYllxditFS1hWZWptVjhxWUEwSVZkWGRBYm1RRHF5dUE1NHRsQjRQQk5ySFh1SWZWdEtUV05mRng0UXlndlBMYlVLRlpodEFwREl6MlYxdWRaL1pPelU1MXNQR0N0WGgwaG5EMXQxZE9LNkl3enJIQml4dys0RGdBOFZEV2FqYm95aVdLQUcreFJTWVdjeDJHcnROT2htaEJDWUU4U3ZYbEh6QzdUdnNUTGVoZXNBM1V4RXhNUGQzMmdRQ3pPVGxEVVpjUW14bmNLSFdxNXM0VlFvUXpEbnpWRHJxeEVYREdyZTJqMXJWVUpRNmpKZ29lYTRmRFcrOHdwMkR1Uk8vT0J5cVp4d253Zy0tQWJsaVJjd1ZMc2FObVk0b25MUDlWdz09--d3fcd1c1cdda3ab462afda7a652cc72e641d150b",
    }

response = requests.request("GET", url, headers=headers)

print(response.status_code)
cookie_jar = response.cookies
cookies = cookie_jar.items()
print(cookies)
print(cookies[0])
print(cookies[0][1])

