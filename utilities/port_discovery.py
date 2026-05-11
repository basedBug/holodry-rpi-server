from utilities.serial_scanner import find_device_port_by_pid_vid
from typing import Final
from time import sleep

# This is from the COM port of the ESP32-S3
ESP32_S3_VID: Final[int] = 0x1A86
ESP32_S3_PID: Final[int] = 0x55D3

# This is from the USB port of the ESP32-S3
# ESP32_S3_VID: Final[int] = 0x303A
# ESP32_S3_PID: Final[int] = 0x1001

RASPBERRY_PI_PICO_VID: Final[int] = 0x2E8A
RASPBERRY_PI_PICO_PID: Final[int] = 0x000A

esp32_s3_port = None
raspberry_pi_pico_port = None


def search_controller_ports() -> None:
    global esp32_s3_port
    global raspberry_pi_pico_port

    # Scan for serial ports connected to the ESP32-S3 and RASPBERRY PI PICO boards

    print("Scanning for critical external controllers")

    while not (esp32_s3_port and raspberry_pi_pico_port):
        if esp32_s3_port is None:
            esp32_s3_port = find_device_port_by_pid_vid(ESP32_S3_VID, ESP32_S3_PID)
            if esp32_s3_port:
                print("Holodry Dryer Controller found")
            else:
                print("Error: No Holodry Dryer Controller found")

        if raspberry_pi_pico_port is None:
            raspberry_pi_pico_port = find_device_port_by_pid_vid(RASPBERRY_PI_PICO_VID, RASPBERRY_PI_PICO_PID)
            if raspberry_pi_pico_port:
                print("OpenFlexure Sangaboard Controller found")
            else:
                print("Error: No OpenFlexure Sangaboard Controller found")

        if not (esp32_s3_port and raspberry_pi_pico_port):
            print("Awaiting retry...")
            sleep(5)  # Wait for 5 seconds to avoid spamming the console

    print("All controllers found. Proceeding...")


def wait_for_dryer_controller_port() -> str | None:
    """Wait only for the Holodry Dryer Controller and return its port."""
    global esp32_s3_port
    while esp32_s3_port is None:
        esp32_s3_port = find_device_port_by_pid_vid(ESP32_S3_VID, ESP32_S3_PID)
        if esp32_s3_port:
            print("Holodry Dryer Controller found")
            return esp32_s3_port
        print("Holodry Dryer Controller not found, retrying in 5 seconds...")
        sleep(5)


def wait_for_sangaboard_controller_port() -> str | None:
    """Wait only for the Sangaboard (Pico) and return its port."""
    global raspberry_pi_pico_port
    while raspberry_pi_pico_port is None:
        raspberry_pi_pico_port = find_device_port_by_pid_vid(RASPBERRY_PI_PICO_VID, RASPBERRY_PI_PICO_PID)
        if raspberry_pi_pico_port:
            print("OpenFlexure Sangaboard Controller found")
            return raspberry_pi_pico_port
        print("Sangaboard not found, retrying in 5 seconds...")
        sleep(5)


def get_dryer_controller_port() -> str | None:
    return esp32_s3_port


def get_sangaboard_controller_port() -> str | None:
    return raspberry_pi_pico_port
