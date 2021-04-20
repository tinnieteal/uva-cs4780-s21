import json

if __name__ == '__main__':
    # Opening JSON file
    file_in = open("all_beauty_old.json", "r")

    # returns JSON object as
    # a dictionary
    data = json.load(file_in)

    # Iterating through the json
    # list
    for i in data:
        i["model"]="item"
        print(i)

        # Closing file
    with open("new.json", "w") as outfile:
        json.dump(data, outfile)
    file_in.close()