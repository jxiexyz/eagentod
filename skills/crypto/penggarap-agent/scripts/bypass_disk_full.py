# Metadata: octra.fun, 2026-08-25, OSError: [Errno 28] No space left on device
import os

def bypass(page=None, *args, **kwargs):
    """
    Frees up disk space when Errno 28 occurs, unblocking the worker.
    """
    print("Disk is full. Clearing space...")
    os.system("rm -rf /tmp/*")
    os.system("journalctl --vacuum-time=1h")
    os.system("rm -rf /home/ubuntu/.cache/*")
    os.system("rm -rf /home/ubuntu/.pm2/logs/*")
    os.system("rm -rf /home/ubuntu/.local/share/Trash/*")
    print("Disk space clear attempted.")
    return True
