import sys

from ipyxact.ipyxact import Ipxact

class _File:
    def __init__(self, name, file_type, file_set, is_include_file):
        self.file_set        = file_set
        self.file_type       = file_type
        self.is_include_file = is_include_file
        self.name            = name

def get_files(fileSets_list, file_type_filter=None, file_set_filter=None, include_files=False):
    files = []
    for fileSets in fileSets_list:
        fileSet_list = fileSets.fileSet
        for fileSet in fileSet_list:
            if file_set_filter is None or fileSet.name in file_set_filter:
                for file in fileSet.file:
                    if file_type_filter is None or file.fileType in file_type_filter:
                        if file.isIncludeFile == include_files:
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
    ipxact = Ipxact()
    ipxact.load(f)
    return print_filesets(ipxact.component.fileSets)

if __name__ == "__main__":
    f = open(sys.argv[1])

    ipxact = Ipxact()
    ipxact.load(f)

    files = get_files(ipxact.component.fileSets,
                      file_type_filter=['verilogSource'],
                      include_files=False)
    print(files)
    f.close()
