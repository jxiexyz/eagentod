import os
import fcntl
import time
import json

LOCK_DIR = "/tmp"
LOCK_FILE_PREFIX = "hermes_browser.lock"
LOCK_PATH = os.path.join(LOCK_DIR, LOCK_FILE_PREFIX)

# Rebut paksa kalau lock dipegang >66 menit (1.1 jam) DAN holder masih hidup.
# Worker plafon = 60 menit, jadi 66 menit = margin 6 menit.
HOLDER_TIMEOUT = 3960

# LLM agent jobs handoff timeout (25 menit).
# Feeder script exit setelah print tasks, tapi LLM agent turn jalan sesudahnya.
# Lock tetap valid selama waktu ini kecuali di-release eksplisit oleh agent.
AGENT_TIMEOUT = 1500
AGENT_JOBS = {"raffle-agent", "eagent-scanner"}

# Guard anti-overlap: satu instance feeder saja per job.
GUARD_DIR = "/tmp"


def is_agent_lock(lock_data: dict) -> bool:
    """Check if lock data represents an LLM agent turn job."""
    if not isinstance(lock_data, dict):
        return False
    return bool(lock_data.get("agent_mode")) or lock_data.get("job_name") in AGENT_JOBS


def is_holder_alive(lock_data: dict) -> bool:
    """Determine if lock holder is currently active."""
    if not isinstance(lock_data, dict):
        return False
    pid = lock_data.get("pid")
    job_name = lock_data.get("job_name", "unknown")
    is_agent = is_agent_lock(lock_data)
    timestamp = lock_data.get("timestamp") or 0
    age = time.time() - timestamp

    if is_agent:
        # Agent job: process PID was the feeder which exits immediately to hand off
        # execution to the LLM agent turn. Active while within AGENT_TIMEOUT.
        return age < AGENT_TIMEOUT
    else:
        # Standard process: holder is alive if PID exists.
        return bool(pid) and os.path.exists(f"/proc/{pid}")


def check_browser_busy():
    """Checks if a browser lock file exists and holder is still alive."""
    if not os.path.exists(LOCK_PATH):
        return False
    try:
        with open(LOCK_PATH, 'r') as f:
            data = json.load(f)
        if is_holder_alive(data):
            return True
        # Stale lock — holder dead or agent timeout exceeded
        release_browser_lock(force=True)
        return False
    except (IOError, json.JSONDecodeError):
        release_browser_lock(force=True)
        return False


def lock_holder_info() -> dict:
    """Returns info about current lock holder, or empty dict if unlocked."""
    if not os.path.exists(LOCK_PATH):
        return {}
    try:
        with open(LOCK_PATH, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {}


def acquire_browser_lock(timeout=5, job_name="momo-worker", holder_timeout=HOLDER_TIMEOUT, agent_mode=None):
    """
    Acquires a browser lock.

    timeout        : batas tunggu (detik). Default 5 = cek sekilas, langsung
                     menyerah kalau ke-lock. Cron berikutnya yang retry (Opsi A).
                     None = tunggu sampai dapat (hindari — feeder dibunuh di 60 menit).
    holder_timeout : kalau lock dipegang >N detik DAN holder masih hidup,
                     anggap wedged -> rebut paksa. Default 3960 (66 menit).
    agent_mode     : True/False override. Default None = auto-detect via AGENT_JOBS.

    Raises RuntimeError if lock cannot be acquired within timeout.
    """
    pid = os.getpid()
    start_time = time.time()
    if agent_mode is None:
        agent_mode = job_name in AGENT_JOBS

    while True:
        try:
            fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            lock_data = {
                "pid": pid,
                "timestamp": time.time(),
                "job_name": job_name,
                "agent_mode": agent_mode
            }
            os.write(fd, json.dumps(lock_data).encode())
            os.close(fd)
            mode_str = " (agent mode)" if agent_mode else ""
            print(f"[LOCK] Acquired browser lock for PID {pid} (job: {job_name}){mode_str}")
            return True
        except FileExistsError:
            # Lock file exists, check its age and process
            try:
                with open(LOCK_PATH, 'r') as f:
                    lock_data = json.load(f)
                locked_pid = lock_data.get("pid")
                locked_job_name = lock_data.get("job_name", "unknown")
                locked_timestamp = lock_data.get("timestamp") or 0

                age = time.time() - locked_timestamp
                is_agent = is_agent_lock(lock_data)
                holder_alive = is_holder_alive(lock_data)

                if not holder_alive:
                    if is_agent:
                        print(f"[LOCK] Stale agent lock found (job: {locked_job_name}, age {age/60:.1f} min > {AGENT_TIMEOUT/60:.1f} min limit). Attempting to clear.")
                    else:
                        print(f"[LOCK] Stale lock found by PID {locked_pid} (job: {locked_job_name}). Attempting to clear.")
                    release_browser_lock(force=True)
                elif not is_agent and holder_timeout is not None and age > holder_timeout:
                    # Holder hidup tapi sudah lewat plafon -> wedged, rebut paksa
                    print(f"[LOCK] WEDGED: PID {locked_pid} (job: {locked_job_name}) held lock "
                          f"{age/60:.1f} min > {holder_timeout/60:.1f} min limit. FORCIBLE RECLAIM.")
                    release_browser_lock(force=True)
                else:
                    if is_agent:
                        print(f"[LOCK] Browser busy. Locked by agent job '{locked_job_name}' since {time.ctime(locked_timestamp)} ({age/60:.1f} min ago).")
                    else:
                        print(f"[LOCK] Browser busy. Locked by PID {locked_pid} (job: {locked_job_name}) since {time.ctime(locked_timestamp)}.")
            except (IOError, json.JSONDecodeError) as e:
                print(f"[LOCK] Error reading lock file: {e}. Attempting to clear.")
                release_browser_lock(force=True)

        if timeout is not None and time.time() - start_time >= timeout:
            raise RuntimeError(f"[LOCK] Could not acquire browser lock within {timeout}s.")

        time.sleep(1)


def release_browser_lock(force=False, job_name=None):
    """
    Releases the browser lock.

    force=False (default): hanya hapus kalau lock memang milik PID ini atau
                           merupakan agent job (dijalankan oleh LLM agent di subprocess baru).
                           Mencegah job lain tidak sengaja melepas lock orang.
    force=True           : hapus apa pun isinya (untuk stale/wedged reclaim).
    """
    try:
        if not os.path.exists(LOCK_PATH):
            return
        if not force:
            try:
                with open(LOCK_PATH, 'r') as f:
                    data = json.load(f)
                locked_pid = data.get("pid")
                locked_job = data.get("job_name")

                if locked_pid == os.getpid():
                    pass
                elif job_name is not None and locked_job == job_name:
                    pass
                elif is_agent_lock(data):
                    pass
                else:
                    return  # bukan milik kita, jangan sentuh
            except (IOError, json.JSONDecodeError):
                pass  # korup -> boleh hapus
        os.remove(LOCK_PATH)
        print(f"[LOCK] Released browser lock.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"[LOCK] Error releasing browser lock: {e}")


def acquire_job_guard(job_name):
    """
    Guard anti-overlap: pastikan hanya 1 instance feeder per job.
    Return file handle (simpan sampai proses selesai), atau None kalau
    instance lain masih jalan.

    Pakai: fcntl.flock(LOCK_EX | LOCK_NB) — otomatis lepas saat proses mati.
    """
    import fcntl
    path = os.path.join(GUARD_DIR, f"hermes_{job_name}.guard")
    try:
        fh = open(path, "w")
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fh
    except (BlockingIOError, OSError):
        return None


if __name__ == "__main__":
    if check_browser_busy():
        print("Browser is currently busy.")
        # Try to acquire, it will report who holds the lock or if it's stale
        try:
            acquire_browser_lock(timeout=10, job_name="test_acquire")
        except RuntimeError as e:
            print(e)
        finally:
            release_browser_lock()
    else:
        print("Browser is not busy.")
        try:
            acquire_browser_lock(job_name="test_job")
            print("Lock acquired for 10 seconds (test).")
            time.sleep(10)
        except RuntimeError as e:
            print(e)
        finally:
            release_browser_lock()
