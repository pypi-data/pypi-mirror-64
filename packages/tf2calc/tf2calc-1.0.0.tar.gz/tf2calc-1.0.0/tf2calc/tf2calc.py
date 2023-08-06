from pricestf import get_price

def prctf_err():
    print("Something went wrong with module 'pricestf' while loading current prices!")
    input("Press any key to quit!")
    quit()

try:
    key_current = get_price("Mann Co. Supply Crate Key")
    earbuds_current = get_price("Earbuds")

    if type(key_current) == type(0) or type(earbuds_current) == type(0):
        prctf_err()
except:
    prctf_err()

key_sell = key_current["sell_price"]["metal"]
earbuds_sell = float(str(earbuds_current["sell_price"]["keys"]) + "." + str(int(round(earbuds_current["sell_price"]["metal"] / key_sell, 2) * 100)))

def calculate(amount, type):
    data = {}
    if type == "scrap":
        data["scrap"] = amount
        data["rec"] = amount / 3
        data["ref"] = amount / 9
        data["key"] = data["ref"] / key_sell
        data["earbuds"] = data["key"] / earbuds_sell
    elif type == "rec":
        data["scrap"] = amount * 3
        data["rec"] = amount
        data["ref"] = amount / 3
        data["key"] = data["ref"] / key_sell
        data["earbuds"] = data["key"] / earbuds_sell
    elif type == "ref":
        data["scrap"] = amount * 9
        data["rec"] = amount * 3
        data["ref"] = amount
        data["key"] = data["ref"] / key_sell
        data["earbuds"] = data["key"] / earbuds_sell
    elif type == "key":
        ref = amount * key_sell
        data["scrap"] = ref * 9
        data["rec"] = ref * 3
        data["ref"] = ref
        data["key"] = amount
        data["earbuds"] = amount / earbuds_sell
    elif type == "earbuds":
        key = amount * earbuds_sell
        ref = key * key_sell
        data["scrap"] = ref * 9
        data["rec"] = ref * 3
        data["ref"] = ref
        data["key"] = key
        data["earbuds"] = amount
    else:
        print("Unknown type: " + type)
        return(0)

    for i in data:
        data[i] = round(data[i], 2)
        
    return(data)
