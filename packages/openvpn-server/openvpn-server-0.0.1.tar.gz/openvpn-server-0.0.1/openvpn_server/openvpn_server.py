import logging
import subprocess
import time
from typing import ByteString

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OpenVPNServer:
    def __init__(self, config_path: str, openvpn_binary: str = "openvpn"):
        self._stdout: ByteString = b""
        self._stderr: ByteString = b""

        logger.debug("Spawning process %s %s", openvpn_binary, config_path)
        self._proc = subprocess.Popen(
            [openvpn_binary, config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # TODO check stdout for service readiness
        logger.debug("Process spawned, PID %s", self._proc.pid)

    def stop(self) -> None:
        if not self.is_running:
            return
        for _ in range(3):
            if self.is_running:
                logger.debug("Process is alive, terminating")
                self._proc.terminate()
                time.sleep(0.1)
                if not self.is_running:
                    break
                time.sleep(2)
        if self.is_running:
            logger.debug("Process is still alive, time to kill it")
            self._proc.kill()
        self._stdout, self._stderr = self._proc.communicate()

    @property
    def is_running(self) -> bool:
        exit_code = self._proc.poll()
        if exit_code is None:
            return True
        return False

    @property
    def stdout(self) -> ByteString:
        self._stdout, self._stderr = self._proc.communicate(timeout=0.01)
        return self._stdout

    @property
    def stderr(self) -> ByteString:
        self._stdout, self._stderr = self._proc.communicate(timeout=0.01)
        return self._stderr
