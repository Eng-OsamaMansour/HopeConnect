import os

# Define your project root directory
project_root = '.'  # <-- Change this to your Django project root
output_file = 'merged_project.txt'
script_name = os.path.basename(__file__)  # Name of this script

# File extensions to include (common in Django projects)
allowed_extensions = [
    '.py',          # Python source files
    '.html',        # Django templates
    '.js', '.ts',   # Frontend scripts
    '.css',         # Stylesheets
    '.json',        # Config or data
    '.txt',         # Requirements or misc
    '.md',          # Docs like README.md
    '.xml',         # Sometimes used in config
]

# Folders to ignore (Django-specific additions)
excluded_dirs = {
    'node_modules', '.git', '__pycache__', '.venv', 'env', 'venv',
    'migrations', 'static', 'media','staticfiles','.dot','.csv','.json '
}

with open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk(project_root):
        # Exclude unwanted folders
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file == script_name:
                continue  # Skip this script itself
            if any(file.endswith(ext) for ext in allowed_extensions):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, project_root)
                outfile.write(f"\n--- FILE: {relative_path} ---\n\n")
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                except Exception as e:
                    outfile.write(f"[Error reading file: {e}]\n\n")

print(f"\n✅ All Django project code merged into: {output_file}")
