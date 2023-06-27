import os

def extract_code_files(folder_path, output_file):
    script_file = os.path.basename(__file__)  # Name der aktuellen Skriptdatei
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(folder_path):
            # Ausschließen der Ordner "static" und "node_modules"
            if 'static' in dirs:
                dirs.remove('static')
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            
            for file in files:
                file_path = os.path.join(root, file)
                if is_code_file(file_path) and file != script_file:
                    relative_path = os.path.relpath(file_path, folder_path)
                    f.write(f"{relative_path}:\n")
                    with open(file_path, 'r') as code_file:
                        code_content = code_file.read()
                        f.write(code_content)
                    f.write("\n\n")

def is_code_file(file_path):
    # Define the file extensions for code files
    code_extensions = ['.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.js']
    return any(file_path.endswith(ext) for ext in code_extensions)

# Specify the folder path and output file name
folder_path = os.path.dirname(os.path.abspath(__file__))
output_file = 'code_contents.txt'

# Call the function to extract code files and save their contents
extract_code_files(folder_path, output_file)