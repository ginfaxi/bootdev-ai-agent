from functions.get_files_info import get_files_info


def print_result(label: str, working_directory: str, directory: str) -> None:
    """Helper to call get_files_info and print in the desired format."""
    result = get_files_info(working_directory, directory)
    print(f'get_files_info("{working_directory}", "{directory}"):')
    print(label)

    if result.startswith("Error:"):
        # Indent error with 4 spaces 
        print(f"    {result}")
    else:
        # Indent each directory with 2 spaces 
        for line in result.splitlines():
            print(f"  {line}")
    print()  # line break


def main():
    print_result(
        'Result for current directory:',
        "calculator",
        ".",
    )

    print_result(
        "Result for 'pkg' directory:",
        "calculator",
        "pkg",
    )

    print_result(
        "Result for '/bin' directory:",
        "calculator",
        "/bin",
    )

    print_result(
        "Result for '../' directory:",
        "calculator",
        "../",
    )


if __name__ == "__main__":
    main()
