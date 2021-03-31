# import os
import socket
import platform


def print_python_env():
    print('-------------------------------------------------------------')
    print('Interpreter')
    print('platform.python_version:    ', platform.python_version())
    print('platform.python_compiler:   ', platform.python_compiler())
    print('platform.python_build:      ', platform.python_build())
    print()
    print('Platform')
    print('platform.platform(Normal):  ', platform.platform())
    print('platform.platform(Aliased): ', platform.platform(aliased=True))
    print('platform.platform(Terse):   ', platform.platform(terse=True))
    print()
    print('Operating System and Hardware Info')
    print('platform.uname:             ', platform.uname())
    print('platform.system:            ', platform.system())
    print('platform.node:              ', platform.node())
    print('platform.release:           ', platform.release())
    print('platform.version:           ', platform.version())
    print('platform.machine:           ', platform.machine())
    print('platform.processor:         ', platform.processor())
    print()
    print('Executable Architecture')
    print('platform.architecture:      ', platform.architecture())
    # print()
    # print('OS')
    # print('os.uname:                   ', os.uname())
    # print('os.getcwd:                  ', os.getcwd())
    print()
    print('Network')
    print('socket.gethostname:         ', socket.gethostname())
    print('socket.gethostbyname        ', socket.gethostbyname(socket.gethostname()))
    print('-------------------------------------------------------------')


def main():
    print_python_env()


if __name__ == '__main__':
    main()
