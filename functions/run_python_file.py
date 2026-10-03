import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified python-file relative to a working directory with arguments as a subprocess, outputting the result of the execution",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "Optional parameter. An array of items which are strings. Every item represents an arguments which is passed to the python file",
                },
            },
            "required": ["file_path"],
            "additionalProperties": ["args"]
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        # print(target_file)
        # print(f"IsDir: {os.path.isdir(target_file)}")

        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        filename, file_extension = os.path.splitext(file_path)
        if file_extension != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command: list[str] = ["python", target_file]
        if args != None:
            command.extend(args)

        complete_process = subprocess.run(command, check=True, cwd=working_directory, capture_output=True, text=True, timeout=30)

        return_val: list[str] = []
        if complete_process.returncode != 0:
            return_val.append(f"Process exited with code {complete_process.returncode}")
        if complete_process.stdout == "" and complete_process.stderr == "":
            return_val.append("No output produced")
        if complete_process.stdout != "":
            return_val.append(f"STDOUT: {complete_process.stdout}")
        if complete_process.stderr != "":
            return_val.append(f"STDERR: {complete_process.stderr}")
        return "\n".join(return_val)


    except Exception as e:
        return f"Error: executing python file: {e}"
