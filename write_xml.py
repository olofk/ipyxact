import sys

from ipyxact.ipyxact import Ipxact

if __name__ == "__main__":
    f = open(sys.argv[1])

    ipxact = Ipxact()
    print("==Loading==")
    ipxact.load(f)

    ipxact.component.vendor = "testing"
    f.close()

    print("==Writing==")
    ipxact.write(sys.argv[2])
