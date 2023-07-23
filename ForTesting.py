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













dictList = {
    "id": 0,
    "list": [
        1,
        1,
        1,
        1,
        1,
    ],
    "count": 1+1-1
}

listTest = [1, 1, 1]

print(listTest)
