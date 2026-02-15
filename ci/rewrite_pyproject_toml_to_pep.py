"""SYNC poetry group dependencies in pyproject.toml
from [tool.poetry.group.*.dependencies]  to -> [project.optional-dependencies]
from [tool.poetry.group.dev.dependencies]  to -> [project.dependency-groups]
"""

import tomlkit
from pathlib import Path
from copy import deepcopy


def is_sem_version(input_str: str) -> bool:
    """Return true or false if a string is a SEM version"""
    try:
        tuple(map(int, (input_str.split("."))))
    except Exception:
        return False
    return True


def convert_poetry_format_to_pep(
    toml_path, output_toml_path: Path | None = None, remove_poetry_optional_deps: bool = False
) -> None:
    """Convert Poetry dependencies to PEP standard
    :param toml_path: input path
    :param output_toml_path: output path
    :param remove_poetry_optional_deps: if set to True then optional groups are ignore.

    example: Below poetry is ignored
    [tool.poetry.group.dev]
    optional= true

    :return: None
    """
    path = Path(toml_path)
    if not path.exists():
        print(f"Error: {toml_path} not found.")
        return

    output_toml_path = output_toml_path if output_toml_path else path

    # Load with tomlkit to preserve formatting/comments
    with open(path, encoding="utf-8") as f:
        config = tomlkit.load(f)

    warning_message = f"""
#This Section added automatically added using script: {Path(*Path(__file__).parts[-2:])}
#####DO NOT CHANGE MANUALLY#####
#use `poetry` commands regularly, PEP sections will be written by the above script
#if the pyproject.toml is changed run `task rewrite-pyproject-toml`
        """

    if config.get("tool", {}).get("poetry", {}).get("scripts"):
        if config.get("project", {}).get("scripts"):
            del config["project"]["scripts"]

        config["project"]["scripts"] = tomlkit.table()
        config["project"]["scripts"] = deepcopy(config["tool"]["poetry"]["scripts"])
        config["project"]["scripts"].comment(warning_message)

    if "optional-dependencies" in config["project"]:
        del config["project"]["optional-dependencies"]

    if "dependency-groups" in config["project"]:
        del config["project"]["dependency-groups"]

    config["project"]["optional-dependencies"] = tomlkit.table()
    config["project"]["dependency-groups"] = tomlkit.table()
    optional_deps = config["project"]["optional-dependencies"]

    if not optional_deps.get("comment"):
        optional_deps.comment(warning_message)
    if not config["project"]["dependency-groups"].get("comment"):
        config["project"]["dependency-groups"].comment(warning_message)

    # Locate Poetry groups
    poetry_tool = config.get("tool", {}).get("poetry", {})
    groups = poetry_tool.get("group", {})

    groups_to_rewrite = []

    for group_name, group_data in groups.items():
        deps = group_data.get("dependencies", {})
        if not deps:
            continue

        extra_list = []
        for pkg, constraint in deps.items():
            # Convert Poetry table format to PEP 508 string format
            if isinstance(constraint, dict):
                version = constraint.get("version", "*")
                # Add basic support for markers/optional_deps if they exist
                marker = f"; {constraint['markers']}" if "markers" in constraint else ""
                extra_list.append(f"{pkg} ({version}){marker}")
            else:
                if "^" in constraint:
                    constraint = constraint.replace("^", "==")

                elif is_sem_version(constraint):
                    constraint = f"=={constraint}"

                extra_list.append(f"{pkg}{constraint}")

        # Add to project.optional-dependencies
        if group_name == "dev":
            config["project"]["dependency-groups"]["dev"] = extra_list
        else:
            optional_deps[group_name] = extra_list
        groups_to_rewrite.append(group_name)

    if remove_poetry_optional_deps:
        # Clean up the old groups
        for group_name in groups_to_rewrite:
            del config["tool"]["poetry"]["group"][group_name]

        # If the group table is now empty, remove it entirely
        if not config["tool"]["poetry"]["group"]:
            del config["tool"]["poetry"]["group"]

    # Write back to file
    with open(output_toml_path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(config))

    print(f"Successfully converted {len(groups_to_rewrite)} groups to optional-dependencies.")


if __name__ == "__main__":
    convert_poetry_format_to_pep(
        Path(Path(__file__).parent.parent, "pyproject.toml"), Path(Path(__file__).parent.parent, "pyproject.toml")
    )
