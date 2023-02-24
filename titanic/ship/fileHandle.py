import os
import re
# from colorhash import ColorHash

filePath = "ship/files/manifest.txt"

def handle_uploaded_file(f):
    if os.path.exists(filePath):
        os.remove(filePath)
    
    with open(filePath, "w") as outfile:
        outfile.write(f.read().decode())
        
def create_file_index():
    listOfContainers = []
    containerNames = []
    i = 0
    
    with open(filePath, "r") as manifest:
        for line in manifest.readlines():
            coordinates = re.findall(r'\[.*?\]', line)[0].replace("[", "").replace("]", "").split(",")
            coordinateTuple = (int(coordinates[0]), int(coordinates[1]))
            weight = int(re.findall(r'\{.*?\}', line)[0].replace("{", "").replace("}", ""))
            name = line.split("}, ")[1].strip()
            
            container = {"row": coordinateTuple[0], "column": coordinateTuple[1], "weight": weight, "name": name}

            listOfContainers.append(container)
            containerNames.append(name)

    return sorted(listOfContainers, key=lambda x: (-x["row"], x["column"])), set(sorted(containerNames))