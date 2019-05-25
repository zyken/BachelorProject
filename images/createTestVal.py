import os
import random
from imutils import paths
from subprocess import call

dir1 = "./labeled_images/"
dir2 = "./labeled_val/"
dir3 = "./train+val/"

call(["mkdir", dir3])

im_paths1 = list(paths.list_images(dir1))
im_paths2 = list(paths.list_images(dir2))

im_paths = im_paths1 + im_paths2

"""
# create dataset train+val
for path in im_paths:
    name = path.split("/")[-1]
    call(["cp", path, dir3+name])
"""

assert(len(im_paths) == len(list(paths.list_images(dir3))))

im_paths = list(paths.list_images(dir3))
im_names = []
im_real_names = []
im_count = []

for path in im_paths:
    real_name = path.replace(dir3, "")
    name = real_name.split("_")[0]
    if name in im_names:
        i = im_names.index(name)
        im_real_names[i].append(real_name)
        im_count[i] += 1
    else:
        im_names.append(name)
        im_count.append(1)
        im_real_names.append([real_name])

assert(len(im_names) == len(im_count))


random.seed(1)
sum_train = 0
sum_val = 0
for name, count, real_names in zip(im_names, im_count, im_real_names):
    train_count = int(0.78*count)
    val_count = int((1.0-0.78)*count)

    random.shuffle(real_names)

    i = 0
    while i < val_count:
        im_path = dir3 + real_names[i]
        call(["mv", im_path, "./shuffled_val/"])
        i += 1
        sum_val += 1
    while i < count:
        im_path = dir3 + real_names[i]
        call(["mv", im_path, "./shuffled_train/"])
        i += 1
        sum_train += 1


print(sum_val, sum_train)