import subprocess


def are_files_equal(file1: str, file2: str) -> bool:
    try:
        res = subprocess.run(["diff", file1, file2], capture_output=True, text=False)

        if res.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
