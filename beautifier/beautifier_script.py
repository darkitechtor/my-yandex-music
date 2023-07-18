import os
from beautifier_module import file_beautifier

directory = "path/to/files/directory"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        try:
            file_beautifier(f)
        except:
            print(f)