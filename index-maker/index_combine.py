import json

def combine_indices():
    with open("./indices.json", "r") as indices:
        data = json.load(indices)

    indeces_to_combine = []
    combined_indices = []

    index_name = input("What should this index be named? ")

    print("What indices should be combined? Available ones are: ", end="")

    for key in data:
        print(key, end=", ")
    print()

    i = 0
    while True:
        i += 1
        added_index = input(f"Index {i} (type exit to cancel): ")
        if added_index == "exit":
            print(indeces_to_combine)
            break
        indeces_to_combine.append(added_index)

    for i in range(len(indeces_to_combine)):
        combined_indices += data[indeces_to_combine[i]]
    
    data[index_name] = list(set(combined_indices))

    with open("./indices.json", "w") as indices:
        json.dump(data, indices, indent=2)

    print("Your indices have been combined")

combine_indices()