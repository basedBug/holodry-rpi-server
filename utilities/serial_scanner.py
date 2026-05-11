from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


def scan_serial_ports() -> None:
    print("Scanning serial ports on system...")

    # Get all serial ports
    ports = list_ports.comports()

    for port in ports:
        # Device path
        print(f"\t {port.device}")
        # Description (fall back to 'n/a' if empty)
        desc: str = port.description or "n/a"
        print(f"\t    desc: {desc}")
        # Hardware ID (fall back to 'n/a' if empty)
        hwid: str = port.hwid or "n/a"
        print(f"\t    hwid: {hwid}")


def find_device_port_by_pid_vid(vid: int = 0x2341, pid: int = 0x0043) -> str | None:
    """
    Find port assigned to device by Vendor ID (VID) and Product ID (PID).
    Defaults to Arduino Uno (VID=0x2341, PID=0x0043).

    Based on https://www.py4u.org/blog/python-to-automatically-select-serial-ports-for-arduino/
    """

    print(f"Searching for ports with device with VID:PID={vid:04X}:{pid:04X}")
    device_matches: list[ListPortInfo] = []

    for port in list_ports.comports():
        if (port.vid == vid) and (port.pid == pid):
            device_matches.append(port)

    if not device_matches:
        print(f"\t No device found with VID:PID={vid:04X}:{pid:04X}")
        return None

    if len(device_matches) > 1:
        port_names: list[str] = [ports.device for ports in device_matches]
        print(
            f"""
            \t Warning: Multiple devices with VID:PID={vid:04X}:{pid:04X} found on ports {port_names}. 
            Returning first instance
            """
        )
    else:
        print(
            f"\t Found device with VID:PID={vid:04X}:{pid:04X} on port {device_matches[0].device}"
        )
    return device_matches[0].device


if __name__ == "__main__":
    # Testing
    scan_serial_ports()
    esp_port = find_device_port_by_pid_vid(vid=0x303A, pid=0x1001)
    print(f"ESP PORT: {esp_port}")
