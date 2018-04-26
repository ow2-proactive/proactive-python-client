

def hello(name=None):
  if name is not None:
    return "Hello " + str(name) + "!"
  else:
    return "Hello world!"


def main():
  hello()


if __name__ == '__main__':
  main()
