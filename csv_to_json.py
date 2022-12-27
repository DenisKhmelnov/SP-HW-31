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

            if "location_id" in row:
                row["locations"] = [row["location_id"]]
                del row["location_id"]

            record["fields"] = row
            jsonArray.append(record)

    with open(jsonFilePath, 'w', encoding="utf-8") as jsonf:
        jsonString = json.dumps(jsonArray, indent=4, ensure_ascii=False)
        jsonf.write(jsonString)


csvFilePathAds = r'./datasets/ad.csv'
jsonFilePathAds = r'./datasets/ad.json'
csv_to_json(csvFilePathAds, jsonFilePathAds, "ads.ad")

csvFilePathCat = r'./datasets/category.csv'
jsonFilePathCat = r'./datasets/category.json'
csv_to_json(csvFilePathCat, jsonFilePathCat, "ads.category")

csvFilePathAds = r'./datasets/user.csv'
jsonFilePathAds = r'./datasets/user.json'
csv_to_json(csvFilePathAds, jsonFilePathAds, "users.user")

csvFilePathCat = r'./datasets/location.csv'
jsonFilePathCat = r'./datasets/location.json'
csv_to_json(csvFilePathCat, jsonFilePathCat, "users.location")
