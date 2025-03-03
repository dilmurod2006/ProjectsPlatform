
# test key va month date yordamida key yasash va uni o'qish

key_encode = {
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f",
    "6": "g",
    "7": "h",
    "8": "i",
    "9": "j",
    "v": "v"
}
key_decode = {
    "a": "0",
    "b": "1",
    "c": "2",
    "d": "3",
    "e": "4",
    "f": "5",
    "g": "6",
    "h": "7",
    "i": "8",
    "j": "9",
    "v": "v"
}
def encode(month_date, test_key):
    data = test_key+"v"+month_date
    result = ""
    for i in data:
        result += key_encode[i]
    return result
def decode(key):
    result = ""
    for i in key:
        result += key_decode[i]
    return result.split("v")[1], result.split("v")[0]
def restructure_dict(data):
    result = {}
    for key, value in data.items():
        year = key[:4]  # 2024 ni ajratib olish
        month = key[4:]  # 12 ni ajratib olish
        if year not in result:
            result[year] = {}
        result[year][month] = value
    return result