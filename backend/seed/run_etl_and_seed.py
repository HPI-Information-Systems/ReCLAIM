"""
Executes all ETL scripts which are defined in the ETL_SCRIPTS_TO_EXECUTE list below,
and seeds the neo4j database with the ttl files generated.
"""

import multiprocessing
import os
import shutil
from err.main import main as err_etl_main
from linz.main import main as linz_etl_main
from marburg.main import main as marburg_etl_main
from munich.main import main as munich_etl_main
from wiesbaden.main import main as wiesbaden_etl_main
from seed.seed_database import seed
from seed.seed_database import create_fulltext_indices

ETL_SCRIPTS_TO_EXECUTE = [
    err_etl_main,
    linz_etl_main,
    marburg_etl_main,
    munich_etl_main,
    wiesbaden_etl_main,
]


def run_etl():
    print("Executing ETL scripts...")
    processes = []
    for source_main_function in ETL_SCRIPTS_TO_EXECUTE:
        p = multiprocessing.Process(target=source_main_function)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    run_etl()
    ttl_files = os.listdir()
    for file_name in ttl_files:
        if file_name.endswith(".ttl"):
            shutil.move(
                file_name,
                os.path.join(os.path.dirname(__file__), "data"),
            )
    seed()
    create_fulltext_indices()
