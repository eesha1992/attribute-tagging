import json
from colour import Color
import pandas as pd
from flask import Flask, request

app = Flask(__name__)
productList = []
with open('attributes_data.txt') as f:
    for jsonObj in f:
        productDict = json.loads(jsonObj)
        productList.append(productDict)

# creating corpus
corpus=["Sneakers", "Under" ,"Armour", "Caldera", "Juicy", "Journee","Collection", "Nunn","Bush", "Levi", "Dr.","Scholl", "Jockey",
        "Columbia", "Lee", "Nike", "Aerosoles", "Skechers", "Rocket","Dog", "LifeStride", "Josmo", "Dockers®", "Ryka","Aspen", "Propet",
        "Jockey®","Levi's®","Scholl's","Lee®", "Superlamb", "Fireside","Dearfoams", "New" ,"Balance®", "Reebok", "Koolaburra",
        "Laredo", "Vance", "Co.", "Clarks®", "Georgia", "Nick" ,"Graham", "adidas", "Skechers®", "Dajana"]

def fetchsize(string):
    strings = string.split()[-2]+ " "+string.split()[-1]

    word = strings.split()
    if word[0].isnumeric():
        if word[1].upper():
            size = strings
        else:

            size = word[0]
    else:

        size= word[1]
    return size


def check_color(color):
    try:
        Color(color)
        return True
    except ValueError:
        return False


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))

def fetchcolor(string):
    color = [i for i in string.split(' ') if check_color(i)]
    final_color = listToString(color)
    return final_color


def check_brand(string):
    final_brand=[]
    for word in string.split():

        if word in corpus:

            final_brand.append(word)
    brand = listToString(final_brand)
    return brand


@app.route('/')
def main():
    size_list=[]
    brand_list=[]
    color_list=[]
    name_list=[]
    for product in productList:
        name = product["text"]
        size = fetchsize(name)

        color = fetchcolor(name)

        name = name.replace("[^a-zA-Z0-9®]", " ")
        brand = check_brand(name)

        size_list.append(size)
        brand_list.append(brand)
        color_list.append(color)
        name_list.append(name)

    final_dataframe = pd.DataFrame(
        {'brand': brand_list,
         'size': size_list,
         'color': color_list,
         'name': name_list
        })
    print (final_dataframe)
    data_dict = final_dataframe.to_dict()
    return data_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
