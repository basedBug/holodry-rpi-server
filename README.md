# Fuck microsoft

To use the python extension: https://github.com/microsoft/vscode-python/issues/25820
Also need to set execute permissions to the pet file as it will have its permissions stripped by default

Cant use pylance due to microsoft fuckery, had to use BasedPyright for intellisense support:
https://github.com/detachhead/basedpyright

Results from **uv run python -m serial.tools.list_ports -v**

    /dev/ttyACM0
        desc: USB JTAG/serial debug unit
        hwid: USB VID:PID=303A:1001 SER=D0:CF:13:58:FA:70 LOCATION=1-1.3:1.0
    /dev/ttyACM1
        desc: Pico - Board CDC
        hwid: USB VID:PID=2E8A:000A SER=E660D4A0A73B9226 LOCATION=1-1.2:1.0
    /dev/ttyAMA0
        desc: n/a
        hwid: n/a
    /dev/ttyS0
        desc: n/a
        hwid: n/a
