import config.configurations

testKeyboard = [[], [], [], []]
city_info = [
    {
        "id": 209,
        "title": "Дакка",
        "development": False,
        "shield": False,
        "shieldInfo": False,
        "lifestandard": 60,
        "condition": True,
        "cityId": 49
    },
    {
        "id": 210,
        "title": "Читагонг",
        "development": False,
        "shield": False,
        "shieldInfo": False,
        "lifestandard": 0,
        "condition": False,
        "cityId": 50
    },
    {
        "id": 211,
        "title": "Богра",
        "development": False,
        "shield": False,
        "shieldInfo": False,
        "lifestandard": 0,
        "condition": False,
        "cityId": 51
    },
    {
        "id": 212,
        "title": "Кокс-базар",
        "development": False,
        "shield": False,
        "shieldInfo": False,
        "lifestandard": 60,
        "condition": True,
        "cityId": 52
    }
]
for i, (city, button) in enumerate(zip(city_info, testKeyboard)):
    button.append("-1")
    button.append(f"{i}: {city['title']}")
    button.append("+1")
print(testKeyboard)

for i, city in enumerate(city_info):
    print(f"{i}: {city['title']}")

lvllife = f"{str(city_info[0]['lifestandard']) + ' + 20 %'}"
listTest = [1]
if 3 >= len(listTest) > 0:
    listTest.remove(1)
    print(f"list less 3: {len(listTest)}")
print(listTest)

print(f"\n\n id: {config.configurations.admins['id']}")