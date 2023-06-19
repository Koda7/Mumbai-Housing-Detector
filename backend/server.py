import sys
from region import getRegion, getSuburbs

sys.path.append("C:\\Users\\HP\\miniconda3\\lib\\site-packages")

from flask import Flask, request, make_response
import json

app = Flask(__name__)

@app.route("/getRegion", methods=["POST"])
def getQueryRegion():
    data = dict(request.form)
    print(data)
    new_data = {}
    for key in data:
        if key == "type":
            new_data[key.lower()] = data[key]
        elif key == "budget":
            new_data[key.lower()] = int(data[key])
        else:
            new_data[key.lower()] = float(data[key]) * 0.009
    getSuburbs(new_data)
    if len(new_data) == 2:
        with open("shapefiles/target_region.json", "r") as f:
            region = json.dumps(json.load(f))
    else:
        getRegion(new_data)
        with open("outputs/region.json", "r") as f:
            region = json.dumps(json.load(f))
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.data = json.dumps({"region": region})
    return response


if __name__ == "__main__":
    app.run(port=8080)
