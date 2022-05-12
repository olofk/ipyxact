import sys

from ipyxact.ipyxact import Component

if __name__ == "__main__":
    f = open(sys.argv[1])

    component = Component()
    print("==Loading==")
    component.load(f)

    component.vendor = "testing"
    f.close()

    print("==Writing==")
    component.write(sys.argv[2])
