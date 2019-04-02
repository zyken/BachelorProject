import os
from imutils import paths
from subprocess import call

dir = "./labeled_images/"

imgpaths = list(paths.list_images(dir))

im_names = []
im_count = []

for path in imgpaths:
    name = path.replace("./labeled_images/", "")
    name = name.split("_")[0]
    if name in im_names:
        i = im_names.index(name)
        im_count[i] += 1
    else:
        im_names.append(name)
        im_count.append(1)


assert(len(im_names) == len(im_count))

sum_t = 0
sum_v = 0
for name, count in zip(im_names, im_count):
    t_count = int(count * 0.1)
    v_count = int(count * 0.2)
    i = 0
    while i < t_count:
        im_path = "./labeled_images/" + name + "_" + str(i) + ".jpg"
        call(["mv", im_path, "./test/"])
        i += 1
        sum_t += 1
    while i < v_count+t_count:
        im_path = "./labeled_images/" + name + "_" + str(i) + ".jpg"
        call(["mv", im_path, "./val/"])
        i += 1
        sum_v += 1

print(sum_t, sum_v)
print(sum_t + sum_v)

