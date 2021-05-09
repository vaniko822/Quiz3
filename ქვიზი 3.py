import requests
import json
import sqlite3

conn = sqlite3.connect('capitals-db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS capitals 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            country VARCHAR(20),
            country_domain VARCHAR(20),
            region  VARCHAR(20),
            population INTEGER
            );''')

capital = input("შეიყვანეთ ქალაქის სახელი: ")
url= f"https://restcountries.eu/rest/v2/capital/{capital}"

r = requests.get(url)
print("ბმული: ", r.url)
print("სტატუს კოდი: ", r.status_code)
print("სერვერიდან დამატებითი ინფორმაცია: ", r.headers)

res = r.json()
with open('capitals.json', 'w') as f:
    json.dump(res,f, indent=4)

print("ქვეყნის სახელი: ", res[0]["name"])
print("ქვეყნის საიტის დომენი: ", res[0]["topLevelDomain"][0])
print("ქვეყნის რეგიონი: ", res[0]["region"])
print("ქვეყნის მოსახლეობა: ", res[0]["population"], "ადამიანი")

# ინფორმაციის შენახვა ბაზაში - მე გადავწყვიტე გამეწერა id-ები, რათა მარტივი იყოს დათვლა მონაცემების, ასევე გადავწყვიტე შემენახა ინფორმაცია ქვეყნის სახელი, დომეინი, რეგიონი და მოსახლეობის რაოდენობა.
country = res[0]["name"]
country_domain = res[0]["topLevelDomain"][0]
region = res[0]["region"]
population = res[0]["population"]
c.execute("INSERT INTO capitals (country, country_domain, region, population) VALUES (?, ?, ?, ?)", (country, country_domain, region, population))


conn.commit()
conn.close()
