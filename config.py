import json
def read(policy):
    addPriceTime = ""
    addPrice=""
    with open("./config.json",'r') as f:
        pl = json.load(f)
        new_pl = pl.get(policy)
        for k,v in new_pl.items():
            if k == "addPriceTime":
                addPriceTime = v
            elif k == "addPrice":
                addPrice = v
    return addPriceTime,addPrice

def readID(id):
    with open("./user.json",'r') as f:
        pl = json.load(f)
        idHash = pl.get(id)
        return idHash

if __name__ == "__main__":
  idh = readID("12341234")
  print(idh)


