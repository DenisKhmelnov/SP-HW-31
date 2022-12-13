import csv
import json
import os

def csv_to_json(csvFilePath, jsonFilePath, model):
    jsonArray = []

    with open(csvFilePath, encoding="utf-8") as csvf:
        for row in csv.DictReader(csvf):
            record = {"model": model, "pk": row["id"]}
            del(row["id"])
            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            record["fields"] = row
            jsonArray.append(record)

    with open(jsonFilePath, 'w', encoding="utf-8") as jsonf:
        jsonString = json.dumps(jsonArray, indent=4, ensure_ascii=False)
        jsonf.write(jsonString)


csvFilePathAds = r'./datasets/ads.csv'
jsonFilePathAds = r'./datasets/ads.json'
csv_to_json(csvFilePathAds, jsonFilePathAds, "ads.ads")

csvFilePathCat = r'./datasets/categories.csv'
jsonFilePathCat = r'./datasets/categories.json'
csv_to_json(csvFilePathCat, jsonFilePathCat, "ads.categories")
