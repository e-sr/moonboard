# use the nice tool https://curl.trillworks.com/ 
# to generate the request from chrome "copy to cURL"
import pathlib
import json 

import requests

cookies = {
    '__RequestVerificationToken': '3abKuAtgHR96wpcifvNgtNljS2ppL_INHTIr0SaO68PahmrYD8PeMa1JNJTiUroe68egoyziIcYbDwYxyy_bJoldqMwqf0wiKLbKQrao7JQ1',
    '_ga': 'GA1.2.202038855.1554291645',
    '_gid': 'GA1.2.342823532.1554291645',
    '_MoonBoard': 'Vk3OSjC9VjCiJSWQycJpqv-lp74EtU5FgyMlZHR7MIs5oKp9J5ZxJVAUaZ-LAfZE8Y3Ni12VGFPHkKeFRqUR_NCNDQZQmevda1_lajpnUdOMKFh6FDe9GCId0fuKGpzHCNOiBOEcSjbb025supcVIWjquFlPhC1d96V8VevLgNs5uHcahDA3d6gpg_CfEPeHcnY_w4cri3dy_I9ELepgOpwHRk6XvAL0GbA03tMncLz9KXuqU-A1wiayzBp4XLdHLRDzruJU0ckXvwhvNUu48E4Enm1rWx8BGK251Wi4IjP_MbuV4AQ-s3dgP4fH2zNGqPT2AuUlZt59QLlFTPSr2jGLhF4CfimGJi7VUJ3ejWYwbOqu7JEiqb0ojYsZXShyBxeW9VVQjO8WWkuA77tTkDU4-wGbehV4xCjsMsyewy8Eqntgkruh0yaHrgqFlarPnyKqjcQGaeCHlwiFJS2L9TmnRptNj32dCQwX4KejWBtdJ6_rWlnEIszf_DiRyF6A9CfG7Ijfoym9tBeTvuYL2o-nsCxaohfhzV5z97jEfhI',
    '__atuvc': '3%7C14',
}

headers = {
    'Origin': 'https://www.moonboard.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'it-CH,it;q=0.9,en-CH;q=0.8,en;q=0.7,de-CH;q=0.6,de;q=0.5,it-IT;q=0.4,en-US;q=0.3',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://www.moonboard.com/Problems/Index',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}
with pathlib.Path("remove_keys.json").open("r+") as f:
    remove_key=json.load(f)

def filter_problem(problem):
    for k,v in remove_key.items():
        if isinstance(v,dict):
            for kk in v.keys():
                problem[k].pop(kk)
        else:
            problem.pop(k)

def fetch_problems_page(page, pagesize=500,setup="2016"):
    hold_setup = {"2016":1, "master2017":15}
    data = {
    'sort': '',
    'page': str(page),
    'pageSize': str(pagesize),
    'group': '',
    'filter': f'setupId~eq~{hold_setup[setup]}'
    }   

    response = requests.post('https://www.moonboard.com/Problems/GetProblems', headers=headers, cookies=cookies, data=data)

    rj= response.json()
    if rj.get('Errors') is not None:
        print(f"Error {rj.get('Errors')}")
    d={}
    for problem in rj['Data']:
        filter_problem(problem)
        k = problem.pop('Id')
        d[k]=problem
    return d, rj['Total']


setup =  "master2017"
#setup =  "2016"
filename = f"moonboard_problems_setup_{setup}"
pagelen = 500
max_fetch=30000


fetches = []
found = 0
page = 1

while True:
    print(f"fetch page {page}")
    d,tot = fetch_problems_page(page,pagelen,setup)
    fetches.append(d)
    found+=len(d)
    print(f"Total problem after update: {found}/{tot}.")
    if found==tot or page>(tot/pagelen+1) or found>=max_fetch:
        break    
    page+=1
# 
print(f"concat problems.")
MoonProb ={}
for d in fetches:
    MoonProb.update(d)

print(f"Total problem after concat: {len(MoonProb)}.")
file_p = pathlib.Path(f'{filename}.json')
print(f"Export problems")

with file_p.open('w+') as f:
    json.dump(MoonProb,f,indent=3)
    

