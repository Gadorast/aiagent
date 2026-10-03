from functions.get_file_content import get_file_content


def print_small(message: str,) -> None:
    # print(message)
    if message.startswith("Error:"):
        print(message)
    else:
        print(f"lorem.txt length: {len(message)}")
        print(f"lorem.txt truncated: {'truncated' in message}")

#result = get_file_content("calculator", "lorem.txt")

print_small(get_file_content("calculator", "lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
