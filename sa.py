
item_name = "the price of bitcoin"
k = " bitcoin"
if item_name not in k:
    for item in  item_name.split(sep=" "):
        print(item)
        if item in k or item == k:
            response = True
            break
        response = {item_name:None}

print(response)