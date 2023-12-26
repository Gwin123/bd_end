from datetime import datetime

import yadisk

from constants.config import Y_TOKEN


async def create_backup():
    disk = yadisk.YaDisk(token=Y_TOKEN)

    disk.upload("database/people.db", f"backup/back_up{datetime.now()}.db")

    print("success")
