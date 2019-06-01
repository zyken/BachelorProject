import os
from shutil import copyfile
from CSVBeetleData import getBeetlesFromCSV

class TreeHandler:
    def __init__(self, root_path, beetles, tree_structure):
        self.root_path = root_path
        self.beetles = beetles
        self.tree_structure = tree_structure

    def moveFolder(self, directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if not self.moveFile(file_path):
                print(file_path)

    def moveFile(self, file_path):
        file_name = os.path.basename(file_path)
        name_without_extension = os.path.splitext(file_name)[0]
        dash_index = name_without_extension.find("_")
        name_without_extension = name_without_extension[:dash_index]
        for beetle in self.beetles:
            if beetle.species.lower() == name_without_extension.lower():
                self.moveBeetle(file_path, beetle)
                return True
        return False

    def moveBeetle(self, old_file_path, beetle):
        file_name = os.path.basename(old_file_path)
        new_file_path = self.root_path

        for attr_name in self.tree_structure:
            new_file_path = new_file_path + "/" + getattr(beetle, attr_name)
            self.checkAndCreateDir(new_file_path)

        new_file_path = new_file_path + "/" + file_name

        copyfile(old_file_path, new_file_path)

    def checkAndCreateDir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)


if __name__ == "__main__":
    tree_level = "genus"
    beetles = getBeetlesFromCSV("../excel/BillebankDatabase2.csv")
    treeHandler = TreeHandler("../../../images/images_" + tree_level + "_shuffled/train", beetles, [tree_level])
    treeHandler.moveFolder("../../../images/shuffled_train")

    beetles = getBeetlesFromCSV("../excel/BillebankDatabase2.csv")
    treeHandler = TreeHandler("../../../images/images_" + tree_level + "_shuffled/val", beetles, [tree_level])
    treeHandler.moveFolder("../../../images/shuffled_val")



