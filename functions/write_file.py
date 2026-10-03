import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File to write the content to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the specified file"
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        # print(target_file)
        # print(f"IsDir: {os.path.isdir(target_file)}")

        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # print(f"Path: {os.path.dirname(target_file)}")

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: write file: {e}"
