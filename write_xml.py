import sys

from ipyxact.ipyxact import Ipxact

if __name__ == "__main__":
    f = open(sys.argv[1])

    ipxact = Ipxact()
    ipxact.load(f)

    f.close()

    ipxact.write('new.xml')
