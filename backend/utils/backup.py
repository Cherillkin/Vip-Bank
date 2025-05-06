import os
import subprocess
from datetime import datetime

def backup_database(
    db_name: str,
    user: str,
    output_dir: str,
    host: str = "localhost",
    port: int = 5438
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{db_name}_backup_{timestamp}.sql"
    output_path = os.path.join(output_dir, filename)

    try:
        pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"  # <-- Укажи свой путь

        result = subprocess.run(
            [
                pg_dump_path,
                "-h", host,
                "-p", str(port),
                "-U", user,
                "-F", "c",
                "-f", output_path,
                db_name,
            ],
            env={**os.environ, "PGPASSWORD": os.getenv("PGPASSWORD", "")},
            check=True
        )
        return {"status": "success", "path": output_path}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
