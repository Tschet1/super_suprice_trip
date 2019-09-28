def get_categories(event_id):
    import json
    with open("data/guidle/category.json", "r") as file:
        data = json.load(file)
    with open("data/guidle/event_category.json", "r") as file:
        data2= json.load(file)

    for idx2 in data2:
        if idx2["event_id"] == event_id:
            event_value = idx2['category_id']
    try:
        while event_value is not None:
            for idx in data:
                for key,value in idx.items():
                    if key == 'category_id' and value == event_value:
                        event_value = idx['parent_category_id']
                        if event_value is None:
                            return idx['title_en']

    except UnboundLocalError:
        return 'Undefined'


"""  #LIST ALL CATEGORIES
import json
with open("data/guidle/category.json", "r") as file:
    data = json.load(file)
with open("data/guidle/event_category.json", "r") as file:
    data2 = json.load(file)

for idx in data:
    for key,value in idx.items():
        if key == "parent_category_id" and value is None:
             print(idx["title_en"])"""

"""#TEST
print(get_categories(1))"""
