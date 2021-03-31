import sys


def hello(name=None):
    if name is not None:
        return "Hello " + str(name) + "!"
    else:
        return "Hello world!"


def main():
    print(hello())

    for arg in sys.argv[1:]:
        print(hello(arg))


if __name__ == '__main__':
    main()
