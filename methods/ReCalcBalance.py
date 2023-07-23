def BalanceCalc(countryInfo: dict, balance):
    countryInfo['balanceInfo'] = balance
    countDevelop = 0
    countShield = 0
    for fCity in countryInfo['friendlyCities']:
        if fCity['development']:
            countDevelop += 1
        if fCity['shield']:
            countShield += 1

    countryInfo['balanceInfo'] -= countDevelop * 150
    countryInfo['balanceInfo'] -= countShield * 300
    if countryInfo['nuclearProgramInfo'] is False and countryInfo['nuclearProgram']:
        countryInfo['balanceInfo'] -= 500
    countryInfo['balanceInfo'] -= 150 * countryInfo['rocket']
    countryInfo['balanceInfo'] -= 150 * countryInfo['ecology']

    for eCountry in countryInfo['enemyCountries']:
        countryInfo['balanceInfo'] -= eCountry['moneyTransfer']


