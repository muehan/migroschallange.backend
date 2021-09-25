

from models import basket, customer


if __name__ == '__main__':
    customers = []
    baskets = []

    with open('../data/ShoppingCart/Abverkaufdaten_trx_202001.csv') as f:
        for line in f.readlines():
            columns = line.split(',')
            if columns[1] == "101324":
                customer = next((x for x in customers if x.id == columns[1]), None)
                if customer == None:
                    customer = customer(columns[1])      
                    customers.append(customer)
                basket = basket(columns[3], columns[1], 0)

                

