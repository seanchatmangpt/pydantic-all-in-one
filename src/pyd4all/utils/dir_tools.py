from pathlib import Path


def project_root_dir() -> Path:
    return Path(".").absolute().parent.parent.parent


def source_dir() -> Path:
    return project_root_dir() / "src"


if __name__ == "__main__":
    print(f'hello world {source_dir()}')
