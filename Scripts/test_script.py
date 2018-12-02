import os
path="../BigBaseline/plaindata/Culture"
print(os.listdir(path))
dir_no=sum(os.path.isdir(path+"/"+i) for i in os.listdir(path))
print(dir_no)
print(os.path.isdir())