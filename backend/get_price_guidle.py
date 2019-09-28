def get_price(event_id):
    import json
    import re
    with open("data/guidle/event.json", "r") as file:
        data = json.load(file)

    for idx in data:
        if idx["event_id"] == event_id:
            price_text = idx["price_information"]
            price_list = (re.findall(r'\d+',price_text))
            price_int = [int(elements) for elements in price_list]
            price = max(price_int)
            return price


    return "No information"


"""#Test
event_id = 1480313
print(get_price(event_id))"""