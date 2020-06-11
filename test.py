import os

if __name__ == '__main__':
    # str1 = "/Users/to2bage/downloads/aaa/ccc/Untitled3.ipynb"
    # str2 = "/Users/to2bage/downloads/aaa"
    #
    # index = str2.rfind("/")
    # print(index)
    # print(str1[index+1:])

    # print(os.path.join("/users/apple", "a/b/c", "d/e/f"))

    for roots, dirs, files in os.walk("/users/apple/desktop/max.jpg"):
        print(roots)
        print(dirs)
        print(files)

    pass