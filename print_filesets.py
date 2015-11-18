import sys

from ipyxact.ipyxact import Component

class _File:
    def __init__(self, name, file_type, file_set, is_include_file):
        self.file_set        = file_set
        self.file_type       = file_type
        self.is_include_file = is_include_file
        self.name            = name

def get_files(fileSets, file_type_filter=None, file_set_filter=None, include_files=False):
    files = []
    for fileSet in fileSets.fileSet:
        if file_set_filter is None or fileSet.name in file_set_filter:
            for file in fileSet.file:
                if file_type_filter is None or file.fileType in file_type_filter:
                    if not include_files or file.isIncludeFile == "true":
                        files.append(file.name)
    return files
    
def print_filesets(file_sets, offset=0, name=None):
    s = ""
    for _fileSets in file_sets: 
        fileSet_list = _fileSets.fileSet
        for fileSet in fileSet_list:
            s += fileSet.name
            s += "\n"
            for file in fileSet.file:
                s += "-"+file.name + "\n"
                s += "-"+file.fileType+"\n"
                s += "-"+str(file.isIncludeFile)
    return s

def write_filesets(f):
    component = Component()
    component.load(f)
    return print_filesets(component.fileSets)

if __name__ == "__main__":
    f = open(sys.argv[1])

    component = Component()
    component.load(f)

    files = get_files(component.fileSets,
                      file_type_filter=['verilogSource'],
                      include_files=False)
    print(files)
    f.close()
