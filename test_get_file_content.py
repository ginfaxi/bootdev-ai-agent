from functions.get_file_content import get_file_content
from config import MAX_CHARS

files_to_test = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

def test_lorem_truncation():
    print("get_file_content('calculator', 'lorem.txt')")
    content = get_file_content("calculator", "lorem.txt")

    # Error check
    if content.startswith("Error:"):
        print("  ERROR while reading lorem.txt:")
        print(f"     {content}")
        print()
        return

    print(f"   Length of content: {len(content)}")

    truncation_msg = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    ends_with_truncation = content.endswith(truncation_msg)

    print(f"   Ends with truncation message: {ends_with_truncation}")
    print(f"   Expected truncatio message: {truncation_msg}")
    print()

def test_the_rest():
    for file in files_to_test:
        print(f'get_file_content("calculator", {file})')
        result = get_file_content("calculator", file)
        print(result)
        print()


def main():
    # Attempt truncate first
    test_lorem_truncation()

    # Test other examples
    test_the_rest()

if __name__ == "__main__":
    main()