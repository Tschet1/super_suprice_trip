def get_cost(weights,event_category,price=1,price_limit=1,superprice_flag=False):
    import math
    """activity score: weights(1) (1:active, 0:passive), 
    culture score: weights(2) (1:culture and museum, 0:concert and party),
    For super discount prices: set superprice_flag = true"""
    if event_category in ['Congresses & conferences','Society','Community calendar','Culinary art','This and that','Economy','Undefined']:
        cost = 10000

    elif event_category == 'Customs, Folklore & Celebrations':
        cost = math.fabs(0.5 - weights[0]) + math.fabs(0.5 - weights[1])

    elif event_category == 'Stage':
        cost = math.fabs(0 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'Exhibitions':
        cost = math.fabs(0.1 - weights[0]) + math.fabs(1 - weights[1])

    elif event_category == 'Art & design':
        cost = math.fabs(0.1 - weights[0]) + math.fabs(0.8 - weights[1])

    elif event_category == 'Concert Pop / Rock / Jazz':
        cost = math.fabs(0.75 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'Concert folk music':
        cost = math.fabs(0.6 - weights[0]) + math.fabs(0.1 - weights[1])

    elif event_category == 'Fair & market':
        cost = math.fabs(0.5 - weights[0]) + math.fabs(0.25 - weights[1])

    elif event_category == 'Concerts others':
        cost = math.fabs(0.4 - weights[0]) + math.fabs(0.1 - weights[1])

    elif event_category == 'Religion & Spirituality':
        cost = math.fabs(0.25 - weights[0]) + math.fabs(1 - weights[1])

    elif event_category == 'Party':
        cost = math.fabs(1 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'Sightseeing & city tour':
        cost = math.fabs(0.75 - weights[0]) + math.fabs(0.9 - weights[1])

    elif event_category == 'Sports':
        cost = math.fabs(1 - weights[0]) + math.fabs(0.5 - weights[1])

    elif event_category == 'Classical concert':
        cost = math.fabs(0 - weights[0]) + math.fabs(0.5 - weights[1])

    elif event_category == 'amusement':
        cost = math.fabs(0.75 - weights[0]) + math.fabs(1 - weights[1])

    elif event_category == 'architecture':
        cost = math.fabs(0.5 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'cultural':
        cost = math.fabs(0.5 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'historical':
        cost = math.fabs(0.5 - weights[0]) + math.fabs(0 - weights[1])

    elif event_category == 'natural':
        cost = math.fabs(1 - weights[0]) + math.fabs(0.5 - weights[1])

    elif event_category == 'welness':
        cost = math.fabs(0 - weights[0]) + math.fabs(0.5 - weights[1])

    if price > price_limit:
        cost = 10000
    elif superprice_flag == True:
        cost = cost + 0.25*price/price_limit
    else:
        cost = cost + 0.5*price/price_limit

    return cost


# TEST
"""import backend.get_categories_guidle

weights = [1,0.5]
event_id = 1473037
#price = 1500
#price_limit = 2500
#superprice_flag = False
event_category = backend.get_categories_guidle.get_categories(event_id)
print(event_category)
print(get_cost(weights, event_category))
#print(get_cost(weights, event_category,price,price_limit,superprice_flag))"""

