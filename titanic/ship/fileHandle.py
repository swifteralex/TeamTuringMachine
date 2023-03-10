import os
import re
from datetime import datetime
# from colorhash import ColorHash

filePaths = {
    'manifest': "ship/files/manifest.txt",
    'log': "ship/files/log.txt",
    'outbound': "ship/files/outbound.txt",
    'test': os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
}

def handle_uploaded_file(f):
    if os.path.exists(filePaths["manifest"]):
        os.remove(filePaths["manifest"])
    
    with open(filePaths["manifest"], "w") as outfile:
        outfile.write(f.read().decode())
        
def create_file_index():
    listOfContainers = []
    containerNames = []
    i = 0
    
    with open(filePaths["manifest"], "r") as manifest:
        for line in manifest.readlines():
            coordinates = re.findall(r'\[.*?\]', line)[0].replace("[", "").replace("]", "").split(",")
            coordinateTuple = (int(coordinates[0]), int(coordinates[1]))
            weight = int(re.findall(r'\{.*?\}', line)[0].replace("{", "").replace("}", ""))
            name = line.split("}, ")[1].strip()
            
            container = {"row": coordinateTuple[0], "column": coordinateTuple[1], "weight": weight, "name": name}

            listOfContainers.append(container)
            containerNames.append(name)

    return sorted(listOfContainers, key=lambda x: (-x["row"], x["column"])), set(sorted(containerNames))


def enter_log(textToSubmit):
    textToSubmit = "$[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "]: " + textToSubmit.strip() + "\n"
    
    with open(filePaths["log"], 'a') as logs:
        logs.write(textToSubmit)
        
    

def prepare_outbound_manifest(containerList, shipname):
    sorted(containerList, key=lambda x: (int(x["containerPos"][0]), int(x["containerPos"][1])))
    currentDestination = filePaths["test"] + "/" + shipname.replace(" ", "") + "outbound.txt"
    
    for container in containerList:
        posX = f'{int(container["containerPos"][0]):02d}'
        posY = f'{int(container["containerPos"][1]):02d}'
        position = "[{}, {}]".format(posX,posY)
        weight = "{" + f'{int(container["weight"]):04d}' + "}"
        containerName = container["containerName"]
        
        textToWrite = (", ").join([position, weight, containerName]) + "\n"
        
        with open(currentDestination, 'a') as outbound:
            outbound.write(textToWrite)
