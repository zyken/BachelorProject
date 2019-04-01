import os
from shutil import copyfile
from CSVBeetleData import getBeetlesFromCSV



def moveFolder(prefix_new_file_name, current_beetle_count, directory_path):
    if os.path.isdir(directory_path):
        for file_name in os.listdir(directory_path):
            old_file_path = os.path.join(directory_path, file_name)
            new_file_name = prefix_new_file_name + "_" + str(current_beetle_count) + ".jpg"
            new_file_path = os.path.join("../../../labeled_images", new_file_name)
            copyfile(old_file_path, new_file_path)

            current_beetle_count += 1
    else:
        print("Directory not found!")
        print(directory_path)
    return current_beetle_count


if __name__ == "__main__":
    beetles = getBeetlesFromCSV("../excel/BillebankDatabase2.csv")
    for beetle in beetles:
        current_beetle_count = 0
        for crop_number in beetle.crops:
            cropsFolder = "../../../images/"
            crop_number_int = int(crop_number)
            if crop_number_int < 10:
               cropsFolder  = cropsFolder + "_000" + str(crop_number_int) + "_crops"
            elif crop_number_int < 100:
                cropsFolder = cropsFolder + "_00" + str(crop_number_int) + "_crops"
            else:
                cropsFolder = cropsFolder + "_0" + str(crop_number_int) + "_crops"
            current_beetle_count = moveFolder(beetle.species, current_beetle_count, cropsFolder)
        print(current_beetle_count)



