import aiofiles
import logging
import os

log = logging.getLogger(__name__)


async def load_mdadm(hub):
    """
    Return list of mdadm devices
    """
    file_path = "/proc/mdstat"
    if not os.path.exists(file_path):
        return
    devices = set()

    async with aiofiles.open(file_path, "r") as mdstat:
        async for line in mdstat:
            if line.startswith("Personalities : "):
                continue
            if line.startswith("unused devices:"):
                continue
            if " : " in line:
                devices.add(line.split(" : ")[0])

    if devices:
        log.debug("mdadm devices detected: {}".format(", ".join(devices)))
        hub.corn.CORN.mdadm = sorted(devices)
