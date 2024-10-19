import os
import subprocess
from pathlib import Path

import typer

app = typer.Typer()


@app.command(name="start")
def start_service(module_name="streamer",
                  app_name="create_app",
                  reload=False,
                  use_testbroker=False):
    """Start the FastStream service with an option to use the TestRedisBroker."""
    os.environ["USE_TESTBROKER"] = "true" if use_testbroker else "false"

    command = [
        "faststream",
        "run",
        f"{module_name}:{app_name}",
        "--factory",
        f"--app-dir={Path(__file__).resolve().parent}"
    ]

    if reload:
        command.append("--reload")

    print(command)

    subprocess.run(command)
