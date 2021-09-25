
import dataclasses
import json
from models import basket, customer, sustainability


if __name__ == '__main__':
    customers = []

    with open('../data/ShoppingCart/Abverkaufdaten_trx_202001.csv') as f:
        i = 0
        for line in f.readlines():
            print('start with line: ' + str(i))
            i = i + 1
            columns = line.split(',')
            # if columns[1] == "101324":
            currentCustomer = next((x for x in customers if x.id == columns[1]), None)
            if currentCustomer == None:
                currentCustomer = customer(columns[1], [])
                customers.append(currentCustomer)

            currentBasket = next((x for x in currentCustomer.baskets if x.id == columns[3]), None)
            if(currentBasket == None):
                currentBasket = basket(
                    columns[3],
                    columns[6],
                    0,
                    0,
                    0.0,
                    0.0)
                currentCustomer.baskets.append(currentBasket)
            
            currentBasket.total_co2 += 10
            
            if(i == 1000):
                break

for item in customers:
    item.sustainability = sustainability(
        total_co2 = sum(b.total_co2 for b in item.baskets),
        total_animal_wellfare = sum(b.total_animal_wellfare for b in item.baskets)
    )
    content = json.dumps(dataclasses.asdict(item))
    # print(content)
    with open('./customers/' + str(item.id) + '.json', "w") as f:
        f.write(content)