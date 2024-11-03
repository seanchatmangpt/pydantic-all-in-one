# pyd4all_filesystem_router.py

import os
import re
import importlib
import yaml
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable, Dict, List, Optional, Any
from dslmodel import init_lm, init_instant, init_text

from fastapi import FastAPI
import uvicorn

# --- Utility Functions ---

def list_python_files(directory: Path) -> List[Path]:
    """
    Recursively list all .py files in a directory.
    """
    return [p for p in directory.rglob("*.py")]

def parse_filename(segment: str) -> str:
    """
    Replace brackets in filename (e.g., [user_id].py) with curly braces for dynamic segments (e.g., {user_id}).
    """
    return re.sub(r"\[(\w+)\]", r"{\1}", segment)

def convert_to_route_path(filepath: Path, root_dir: Path) -> str:
    """
    Convert a filepath to a route path by replacing brackets with curly braces and removing the .py extension.
    Treats 'index.py' as the root of the directory it’s in.
    """
    relative_path = filepath.relative_to(root_dir).with_suffix("")
    path_parts = [parse_filename(part) for part in relative_path.parts]

    # Remove 'index' from the path if the file is 'index.py'
    if path_parts[-1] == "index":
        path_parts = path_parts[:-1]

    route_path = "/" + "/".join(path_parts)
    return route_path


def import_module_from_path(module_path: str) -> Any:
    """
    Dynamically import a module from a module path.
    """
    return importlib.import_module(module_path)

def sanitize_segment(segment: str) -> str:
    """
    Sanitize segments by replacing non-alphanumeric characters (except {}) with underscores.
    """
    return re.sub(r"[^a-zA-Z0-9{}]", "_", segment)

# --- Router Registration Functions ---

def register_route(app, path: str, instance: Callable, framework: str):
    """
    Register a route or handler with the application instance based on the framework.
    """
    if framework == "fastapi":
        app.include_router(instance, prefix=path)
    elif framework == "faststream":
        topic = path.replace("/", ".")
        app.subscribe(instance, topic=topic)
    elif framework == "typer":
        app.add_typer(instance, name=path.strip("/").replace("/", "_"))
    else:
        raise ValueError(f"Unsupported framework: {framework}")

# --- Main Route Loading Functions ---

def load_routes(app: Any, root_dir: Path, framework: str, instance_name: str = "router"):
    """
    Traverse the directory structure and load routes or handlers based on the file hierarchy.
    """
    python_files = list_python_files(root_dir)
    base_path = ".".join(root_dir.parts[root_dir.parts.index("pyd4all"):])  # Start path from 'pyd4all'
    for filepath in python_files:
        relative_path = filepath.relative_to(root_dir)
        module_path = f"{base_path}." + ".".join(relative_path.with_suffix("").parts)
        try:
            module = import_module_from_path(module_path)
            instance = getattr(module, instance_name, None)
            if instance:
                route_path = convert_to_route_path(filepath, root_dir)
                register_route(app, route_path, instance, framework)
                print(f"Registered {framework} path: {route_path}")
        except ModuleNotFoundError as e:
            print(f"Failed to import module {module_path}: {e}")


# --- Watcher for Real-time Route Reloading ---

class ModuleReloadHandler(FileSystemEventHandler):
    def __init__(self, app: Any, root_dir: Path, framework: str, instance_name: str = "router"):
        self.app = app
        self.root_dir = root_dir
        self.framework = framework
        self.instance_name = instance_name

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"File modified: {event.src_path}. Reloading routes...")
            load_routes(self.app, self.root_dir, self.framework, self.instance_name)

def start_filesystem_watcher(app: Any, root_dir: Path, framework: str, instance_name: str = "router"):
    """
    Start the filesystem watcher to monitor for file changes and reload routes as needed.
    """
    event_handler = ModuleReloadHandler(app, root_dir, framework, instance_name)
    observer = Observer()
    observer.schedule(event_handler, path=str(root_dir), recursive=True)
    observer.start()
    print(f"Started filesystem watcher for {framework} at {root_dir}")

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

# --- Configuration Loading ---

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load YAML configuration for framework-specific root directories.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# --- Main Command ---

def load_filesystem_routes(app: Any, framework: str, config_path: str = "watcher_config.yaml", instance_name: str = "router"):
    """
    Load routes or handlers based on the filesystem directory structure and optionally start a watcher.
    """
    config = load_config(config_path)
    root_dir = Path(config.get(f"{framework}_folder"))

    if not root_dir.exists():
        print(f"Error: Root directory '{root_dir}' does not exist.")
        return

    # Load initial routes
    load_routes(app, root_dir, framework, instance_name)

    # Start filesystem watcher
    # if framework in ["fastapi", "faststream"]:
    #     start_filesystem_watcher(app, root_dir, framework, instance_name)




# Load routes dynamically from the filesystem

def print_registered_routes(app: FastAPI):
    """
    Print all registered routes in the FastAPI application.
    """
    print("\nRegistered Routes:")
    for route in app.routes:
        print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")


def main():
    """
    Main function to load routes and start the FastAPI server.
    """
    app = FastAPI()

    # Load routes dynamically from the filesystem
    load_filesystem_routes(app, "fastapi", config_path="watcher_config.yaml")

    from fastui import FastUI, AnyComponent, prebuilt_html, components as c

    from fastapi.responses import HTMLResponse

    @app.get('/{path:path}')
    async def html_landing() -> HTMLResponse:
        """Simple HTML page which serves the React app, comes last as it matches all paths."""
        return HTMLResponse(prebuilt_html(title='FastUI Demo'))
    # Print all registered routes
    print_registered_routes(app)

    # Start FastAPI server
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':
    main()
