import sys

from hellopkg.hello import *


def main():
    print(hello())

    for arg in sys.argv[1:]:
        print(hello(arg))


if __name__ == '__main__':
    main()
