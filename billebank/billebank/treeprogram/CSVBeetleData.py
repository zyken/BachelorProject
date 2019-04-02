import csv

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

beetles = getBeetlesFromCSV("../BillebankDatabase2.csv")

