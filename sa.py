
# item_name = "the price of bitcoin"
# k = " bitcoin"
# if item_name not in k:
#     for item in  item_name.split(sep=" "):
#         print(item)
#         if item in k or item == k:
#             response = True
#             break
#         response = {item_name:None}

# print(response)


s=[{'name': 'the price of 2024 range rover', 'price': None, 'image_urls': ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbYahHa9gnAMJe44dqQ2Og23b4wVltaefvH5gTxfOz8IIbDKAz_mcs_Mk&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbnaz6Z5_1uZMqauNvTeYJNS8-FTzTuOzU-DBdxR7T3HTiADBlWBHQ2Q&s', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN5UMJ1FqSulfw9gHMCkaZPWENpVQnkYKGMxcjTeGC9gX_volA1pA-ZBM&s']}]


def filter_results(resultlist):
        filtered_results = []
        for result in resultlist:
            try:
                for key, value in result.items():
                    if key == "price" and value != None:
                            filtered_results.append(result)
                            break
            except Exception as e:
                print(f"Error filtering results: {e}")
        return filtered_results


print(filter_results(s))