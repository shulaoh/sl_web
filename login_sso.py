import requests
from requests import Session
import re

url = "https://gmp.oracle.com/captcha/files/airespace_pwd_apac.txt"
sso_url = "https://login.oracle.com/mysso/signon.jsp"
sso_submit_url = "https://login.oracle.com/oam/server/sso/auth_cred_submit"

proxies = {
    "http" : "http://cn-proxy.cn.oracle.com:80"
         }

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'   
headers = { 'User-Agent' : user_agent, 
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

username = 'test'
password = 'test'

def testing(self):
    parsePayload()
   
def parsePayload(content, regex):
    pattern = re.compile(regex, re.S)
    items = re.findall(pattern, content)
    payload = {}
    for item in items:
        key = item[0];
        value = item[1];
        payload[key] = value
    payload["ssousername"] = username
    payload["password"] = password
    return payload

with requests.Session() as session:
    session.cookies.clear()
    session.headers.update(headers)
    response = session.get(url, 
                           proxies = proxies)
    print("Response Status code: " + str(response.status_code))
    
    content = response.content.decode('utf-8')
    
    regex_string = '<input type="hidden" name="(.*?)" value="(.*?)">'
    
    payload = parsePayload(content, regex_string)
    
    resp = session.post(sso_url, data=payload, headers=headers, proxies = proxies)
    print("SSO Response Status: ", resp.status_code)
    sso_content = resp.content.decode('utf-8')

    regex_string_sso = '<input type="hidden" name="(.*?)" value="(.*?)" />'

    payload = parsePayload(sso_content, regex_string_sso)
    
    submit_response = session.post(sso_submit_url, data=payload)
    
    print("Submit Response Status:", submit_response.status_code)
    content_password = submit_response.content.decode('utf-8')
    #print(content_password)
    
    pa = re.compile("Password: (.*?)\n", re.S)
    password_list = re.findall(pa, content_password)
    password = password_list.pop()
    print(password)
    
