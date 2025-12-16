from functions.write_file import write_file


def main():
    # 1) Overwrite existing lorem.txt
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    print()

    # 2) Create a new file in calculator/pkg
    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    print()

    # 3) Attempt to write outside working directory (should be an error)
    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
    print()


if __name__ == "__main__":
    main()
