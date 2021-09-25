import os.path
import dataclasses
import json
from models import basket, customer, sustainability


def CalculateScore(rating):
    if(rating == 1):
        return 0
    if(rating == 2):
        return 0
    if(rating == 3):
        return 1
    if(rating == 4):
        return 3
    if(rating == 5):
        return 6
    return 0


if __name__ == '__main__':
    customers = []

    with open('../data/ShoppingCart/Abverkaufdaten_trx_202001.csv') as f:
        next(f)
        i = 0
        for line in f.readlines():
            print('start with line: ' + str(i))
            i = i + 1
            columns = line.split(',')
            # if columns[1] == "101324":
            currentCustomer = next(
                (x for x in customers if x.id == columns[1]), None)
            if currentCustomer == None:
                currentCustomer = customer(columns[1], [])
                customers.append(currentCustomer)

            currentBasket = next(
                (x for x in currentCustomer.baskets if x.id == columns[3]), None)
            if(currentBasket == None):
                currentBasket = basket(
                    columns[3],
                    columns[6],
                    0,
                    0,
                    0.0,
                    0.0)
                currentCustomer.baskets.append(currentBasket)
            
            if(os.path.isfile('../data/products/products/de/' + str(columns[8]) + '.json')):
                with open('../data/products/products/de/' + str(columns[8]) + '.json', encoding="utf8") as j:
                    product = json.loads(j.read())
                    if("m_check2" in product):
                        m_check2 = product["m_check2"]
                        if("carbon_footprint" in m_check2):
                            carbon_footprint = m_check2["carbon_footprint"]
                            if("ground_and_sea_cargo" in carbon_footprint):
                                print("found ground and sea cargo")
                                ground_and_sea_cargo = carbon_footprint["ground_and_sea_cargo"]
                                rating = ground_and_sea_cargo["rating"]
                                calculatedScore = CalculateScore(int(rating))
                                sustanable_score = calculatedScore
                                currentBasket.total_co2 += sustanable_score
            else:
                print('product not found: ' + str(columns[8]))
            if(i == 10000):
                break

for item in customers:
    item.sustainability = sustainability(
        total_co2=sum(b.total_co2 for b in item.baskets),
        total_animal_wellfare=sum(
            b.total_animal_wellfare for b in item.baskets)
    )
    content = json.dumps(dataclasses.asdict(item))
    # print(content)
    with open('./customers/' + str(item.id) + '.json', "w") as f:
        f.write(content)
