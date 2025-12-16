from functions.run_python_file import run_python_file


def main():
    # Calculator test with no args (show usage)
    print('run_python_file("calculator", "main.py"):')
    result = run_python_file("calculator", "main.py")
    print(result)
    print()

    # Calculator test with arg
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print()

    # Calculator tests
    print('run_python_file("calculator", "tests.py"):')
    result = run_python_file("calculator", "tests.py")
    print(result)
    print()

    # Attempt to run a file outside working directory (should error)
    print('run_python_file("calculator", "../main.py"):')
    result = run_python_file("calculator", "../main.py")
    print(result)
    print()

    # Non-existent file test (should error)
    print('run_python_file("calculator", "nonexistent.py"):')
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print()

    # Not a Python file  test (should error)
    print('run_python_file("calculator", "lorem.txt"):')
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print()


if __name__ == "__main__":
    main()
