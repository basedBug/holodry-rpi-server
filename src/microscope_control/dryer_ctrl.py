from utilities.port_discovery import wait_for_dryer_controller_port
import logging
import serial
import json
from itertools import islice

logging.basicConfig(
    level=logging.DEBUG,  # Show INFO, WARNING, ERROR, etc.
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# Based on "Parsing Serial Data - JSON" from "https://www.pyserial.com/docs/reading-data"
def read_json_objects(serial: serial.Serial):
    """Yield complete JSON objects from a serial stream."""
    buffer = ""
    depth = 0
    while True:
        char = serial.read(1).decode("utf-8", errors="ignore")

        # Iterate through each character in the newly received chunk
        if not char:
            continue
        buffer += char
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            # When depth goes back to 0 and we have content, we likely have a full object.
            if depth == 0 and buffer.strip():
                # Try to parse the complete JSON object
                try:
                    yield json.loads(buffer)  # Suspend the generator and return the json object
                except json.JSONDecodeError:
                    # In case of unrecoverable error, clear the buffer to avoid getting stuck.
                    buffer = ""
                    pass
                # Clear buffer
                buffer = ""


def test_dryer_controller_reads() -> None:
    board_port = wait_for_dryer_controller_port()

    dryer_comms = serial.Serial(
        board_port,
        921600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0,
    )

    print("Starting reading test...")

    try:
        """ while True:
            # Read until receiving an "\n"
            received_line = dryer_comms.readline()
            print(f"Received line: {received_line}")

            try:
                # Received line needs to be decoded into utf-8 as the read data is encoded as bytes, allegedly
                # also the newline char must be stripped
                decoded_line = received_line.decode("utf-8").strip()
            except UnicodeDecodeError as err:
                print(f"Decoding error: {err} - raw bytes: {received_line}")
                continue

            if not decoded_line:
                continue  # skip empty lines

            try:
                json_data = json.loads(decoded_line)

                print(f"Received data: {json_data}")

                # if not received_line:
                # Timeout
                #    continue

            except json.JSONDecodeError as err:
                print(f"Invalid JSON: {decoded_line} - error: {err}") """

        # Keep reading the ojects, this is infinite as the iterator never stops
        # for json_object in read_json_objects(dryer_comms):

        # Read 3 times (just for testing)
        for json_object in islice(read_json_objects(dryer_comms), 3):
            print(f"Received: {json_object}")

    except KeyboardInterrupt:
        print("\nExiting")

    finally:
        print("Reading test finished")
        dryer_comms.close()
        print("Serial port closed")


if __name__ == "__main__":
    test_dryer_controller_reads()
