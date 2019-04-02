import csv

def fileExists(path):
    try:
        fh = open(path, 'r')
        fh.close()
        return True
    except FileNotFoundError:
        return False

class CSVBeetleData(object):
    def __init__(self, species, genus, tribe, subfamily, family, synonym=""):
        self.species = species
        self.genus = genus
        self.tribe = tribe
        self.subfamily = subfamily
        self.family = family
        self.synonym = synonym


    @staticmethod
    def fromCSVRowArray(row_array):
        if len(row_array) > 0 and row_array[0] != "":
            species = row_array[0]
            genus = row_array[1]
            tribe = row_array[2]
            subfamily = row_array[3]
            family = row_array[4]
            synonym = row_array[13]

            return CSVBeetleData(species, genus, tribe, subfamily, family, synonym)
        else:
            return None

def getBeetlesFromCSV(path):
    with open(path, newline="") as csvfile:
            beetles = []
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            first_row = next(csvreader)
            for row_array in csvreader:
                new_beetle = CSVBeetleData.fromCSVRowArray(row_array)
                if new_beetle is not None:
                    beetles.append(new_beetle)
            return beetles

csvData = []

beetles = getBeetlesFromCSV("../excel/BillebankDatabase2.csv")
for beetle in beetles:
    current_beetle_count = 0
    path = "../../../labeled_images/" + beetle.species + "_" + str(current_beetle_count) + ".jpg"
    while fileExists(path):
        current_beetle_count += 1
        path = "../../../labeled_images/" + beetle.species + "_" + str(current_beetle_count) + ".jpg"
    csvData.append([beetle.species, current_beetle_count])

import csv
with open('histogram.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

    csvFile.close()
