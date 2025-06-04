import subprocess
import time
import signal
import os
from pathlib import Path


def test_streamlit_app_runs():
    """Test that the Streamlit app starts and boots up properly."""
    project_root = Path(__file__).resolve().parent.parent
    app_path = project_root / "app.py"

    assert app_path.exists(), f"❌ app.py not found at: {app_path}"

    # Start the Streamlit app process
    proc = subprocess.Popen(
        ["streamlit", "run", str(app_path), "--server.headless", "true"],
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=os.setsid  # So we can kill it later
    )

    try:
        # Read stdout line-by-line with timeout logic
        start_time = time.time()
        boot_successful = False

        while time.time() - start_time < 10:
            line = proc.stdout.readline()
            if not line:
                continue
            print(f"[streamlit stdout] {line.strip()}")
            if "Local URL:" in line or "Streamlit" in line:
                boot_successful = True
                break

        assert boot_successful, "❌ Streamlit app did not start as expected."
    finally:
        # Cleanly shut down the process group
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        proc.wait(timeout=5)
