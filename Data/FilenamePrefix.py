import os
# the {PrefixName} should be set to what you want the filename to be prefixed with
path = "C:/Path/To/Your/File/{PrefixName}"

for filename in os.listdir(path):
    # This will rename the file by prefixing the name of the directory {PrefixName} (last folder) from the path variable above
    os.rename(os.path.join(path, filename), os.path.join(path, os.path.relpath(path) + "_" + filename))

