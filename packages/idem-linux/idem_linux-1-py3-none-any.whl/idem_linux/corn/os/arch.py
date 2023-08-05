# Build the osarch grain. This grain will be used for platform-specific
# considerations such as package management. Fall back to the CPU architecture.
import shutil


async def get_osarch(hub):
    if shutil.which("rpm"):
        ret = await hub.exec.cmd.run('rpm --eval "${_host_cpu}"')
        hub.corn.CORN.osarch = ret["stdout"].strip() or "unknown"
    elif shutil.which("opkg"):
        archinfo = {}
        for line in (
            await hub.exec.cmd.run(["opkg", "print-architecture"])["stdout"]
        ).splitlines():
            if line.startswith("arch"):
                _, arch, priority = line.split()
                archinfo[arch.strip()] = int(priority.strip())
        # Return osarch in priority order (higher to lower)
        hub.corn.CORN.osarch = sorted(archinfo, key=archinfo.get, reverse=True)
    elif shutil.which("dpkg"):
        hub.corn.CORN.osarch = (await hub.exec.cmd.run("dpkg --print-architecture"))[
            "stdout"
        ].strip()
    else:
        try:
            import platform

            hub.corn.CORN.osarch = "".join([x for x in platform.uname()[-2:] if x][-1:])
        except (ImportError, NameError):
            hub.corn.CORN.osarch = hub.corn.CORN.cpuarch
