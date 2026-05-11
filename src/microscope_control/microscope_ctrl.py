from utilities.port_discovery import wait_for_sangaboard_controller_port
import sangaboard
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Show INFO, WARNING, ERROR, etc.
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def test_sangaboard() -> None:
    board_port = wait_for_sangaboard_controller_port()

    # The sangaboard module manages the serial port by itself once given
    board_ctrl = sangaboard.Sangaboard(board_port)
    if board_ctrl.test_communications():
        print("Communications successful")


if __name__ == "__main__":
    test_sangaboard()
