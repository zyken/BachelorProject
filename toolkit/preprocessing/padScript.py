from padImg import PadImageWhite
import cv2
import os
from subprocess import call

def padScript(rootdir, new_aug_root):
    call(["mkdir",  new_aug_root])
    i = 0
    for subdir, dirs, files in os.walk(rootdir):
        if i == 0:
            i += 1
            continue

        new_dir = os.path.join(new_aug_root, subdir.split(os.path.sep)[-1])
        call(["mkdir",  new_dir])

        for file in files:
            file_path = os.path.join(subdir, file)
            im = cv2.imread(file_path)
            im = PadImageWhite(im, 1644, 1644)
            sub_folder = os.path.join(new_aug_root, file_path.split(os.path.sep)[-2])
            new_file_path = os.path.join(sub_folder, file)
            print(new_file_path)
            cv2.imwrite(new_file_path, im)

padScript("../../images/images_genus", "../../images/augmented_images/images_genus")
