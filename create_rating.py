import os.path
import dataclasses
import json
from models import basket, customer, sustainability, rating


def CalculateScore(rating, amount):
    if(rating == 1):
        return 0
    if(rating == 2):
        return 0
    if(rating == 3):
        return 1 * amount
    if(rating == 4):
        return 3 * amount
    if(rating == 5):
        return 6 * amount
    return 0


if __name__ == '__main__':
    customers = []

    with open('../data/ShoppingCart/Abverkaufdaten_trx_202001.csv') as f:
        next(f)
        i = 0
        for line in f.readlines():
            if i % 10000 == 0:
                print(i)
            i = i + 1
            columns = line.split(',')
            # if columns[1] != "108248":
            #     continue
            currentCustomer = next(
                (x for x in customers if x.id == columns[1]), None)
            if currentCustomer == None:
                currentCustomer = customer(columns[1], [])
                customers.append(currentCustomer)

            currentBasket = next(
                (x for x in currentCustomer.baskets if x.id == columns[2]), None)
            if(currentBasket == None):
                currentBasket = basket(
                    columns[2],
                    columns[6],
                    rating(0, 0, 0),
                    rating(0, 0, 0))
                currentCustomer.baskets.append(currentBasket)

            if(os.path.isfile('../data/products/products/de/' + str(columns[8]) + '.json')):
                with open('../data/products/products/de/' + str(columns[8]) + '.json', encoding="utf8") as j:
                    product = json.loads(j.read())
                    if("m_check2" in product):
                        m_check2 = product["m_check2"]
                        if("carbon_footprint" in m_check2):
                            carbon_footprint = m_check2["carbon_footprint"]
                            if("ground_and_sea_cargo" in carbon_footprint):
                                ground_and_sea_cargo = carbon_footprint["ground_and_sea_cargo"]
                                currentRating = ground_and_sea_cargo["rating"]
                                calculatedScore = CalculateScore(
                                    int(currentRating), float(columns[9]))
                                sustanable_score = calculatedScore
                                currentBasket.rating_co2.total += int(
                                    sustanable_score)
                                currentBasket.rating_co2.count += 1
                        if("animal_welfare" in m_check2):
                            animal_welfare = m_check2["animal_welfare"]
                            currentRating = animal_welfare["rating"]
                            calcualtedAnimalScore = CalculateScore(
                                int(currentRating), float(columns[9]))
                            currentBasket.rating_animal_welfare.total += int(calcualtedAnimalScore)
                            currentBasket.rating_animal_welfare.count += 1
            # else:
            #     print('product not found: ' + str(columns[8]))
            # if(i == 100000):
            #     break

for item in customers:
    item.sustainability = sustainability(
        total_co2=sum(b.rating_co2.total for b in item.baskets),
        total_animal_welfare=sum(
            b.rating_animal_welfare.total for b in item.baskets)
    )

    for basket in item.baskets:
        if basket.rating_co2.total > 0:
            basket.rating_co2.average = basket.rating_co2.total / basket.rating_co2.count
        if basket.rating_animal_welfare.total > 0:
            basket.rating_animal_welfare.average = basket.rating_animal_welfare.total / \
                basket.rating_animal_welfare.count
    content = json.dumps(dataclasses.asdict(item))
    # print(content)
    with open('./customers/' + str(item.id) + '.json', "w") as f:
        f.write(content)
