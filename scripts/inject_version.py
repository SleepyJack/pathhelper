import argparse
import os

version_tag = '"UNKNOWN"'

def replace_version_string(filepath: str, version: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace(f'{version_tag}', f'"{version}"')
    if content == new_content:
        raise ValueError(f"No replacement made in {filepath} — check that {version_tag} appears.")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Inject a version number into project files.")
    parser.add_argument("version", help="Version number to inject (e.g. 0.1.0)")
    args = parser.parse_args()

    version = args.version

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

    pyproject_path = os.path.join(project_root, "pyproject.toml")
    init_path = os.path.join(project_root, "pathtools", "__init__.py")

    replace_version_string(pyproject_path, version)
    replace_version_string(init_path, version)


if __name__ == "__main__":
    main()
