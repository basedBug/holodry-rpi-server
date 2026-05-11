import json
from dataclasses import dataclass, field
from enum import Enum


class MainStatus(str, Enum):
    IDLE = "IDLE"
    TUNING = "TUNING"
    DRYING = "DRYING"
    VENTING = "VENTING"
    EMERGENCY_VENTING = "EMERGENCY_VENTING"
    MANUAL_MODE = "MANUAL_MODE"
    SHOWCASE_MODE = "SHOWCASE_MODE"


class FanState(str, Enum):
    OFF = "OFF"
    ON = "ON"


class VentsState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"


@dataclass
class Status:
    mainStatus: MainStatus = MainStatus.IDLE
    exteriorAbsHum: float = 0.0
    interiorAbsHum: float = 0.0
    heaterSetpoint: float = 0.0
    fan: FanState = FanState.OFF
    vents: VentsState = VentsState.CLOSED


@dataclass
class SystemConfig:
    targetChamberTemp: float = 0.0
    maxAllowedFilamentTemp: float = 60
    targetRelHum: float = 20


# This ones (readings structures) may need to be changed as we dont deal with this structure back
# on the ESP32 JSON structure
@dataclass
class TemperatureReading:
    max: float = 0.0
    avg: float = 0.0


@dataclass
class HumidityReading:
    max: float = 0.0
    avg: float = 0.0


@dataclass
class ChamberState:
    chamberTemp: TemperatureReading = field(default_factory=TemperatureReading)
    chamberHum: HumidityReading = field(default_factory=HumidityReading)


@dataclass
class AmbientState:
    temp: float = 0.0
    hum: float = 0.0


@dataclass
class FilamentState:
    filamentTemp: TemperatureReading = field(default_factory=TemperatureReading)


@dataclass
class ChamberTelemetry:
    sht31_0_temp: float = 0.0
    sht31_0_hum: float = 0.0
    sht31_1_temp: float = 0.0
    sht31_1_hum: float = 0.0
    sht31_2_temp: float = 0.0
    sht31_2_hum: float = 0.0
    ds18b20_temp: float = 0.0


@dataclass
class AmbientTelemetry:
    sht31_3_temp: float = 0.0
    sht31_3_hum: float = 0.0


@dataclass
class FilamentTelemetry:
    mlx90614_0_temp: float = 0.0
    mlx90614_1_temp: float = 0.0


@dataclass
class RawSensorTelemetry:
    chamber: ChamberTelemetry = field(default_factory=ChamberTelemetry)
    ambient: AmbientTelemetry = field(default_factory=AmbientTelemetry)
    filament: FilamentTelemetry = field(default_factory=FilamentTelemetry)


@dataclass
class SystemState:
    status: Status = field(default_factory=Status)
    systemConfig: SystemConfig = field(default_factory=SystemConfig)
    chamberState: ChamberState = field(default_factory=ChamberState)
    ambientState: AmbientState = field(default_factory=AmbientState)
    filamentState: FilamentState = field(default_factory=FilamentState)


@dataclass
class SystemData:
    systemState: SystemState = field(default_factory=SystemState)
    rawSensorTelemetry: RawSensorTelemetry = field(default_factory=RawSensorTelemetry)


# Need to init this somehow
system_data = SystemData()


# Maybe return some structure or edit globals directly?
def parse_incoming_dryer_json(json_string: str):  # pyright: ignore[reportGeneralTypeIssues]
    global system_data

    try:
        # Deserealize the data into a python object
        data = json.loads(json_string)

        # Check every JSON object and key
        if "systemState" in data and isinstance(data["systemState"], dict):
            systemState_ = data["systemState"]

            if "status" in systemState_ and isinstance(systemState_["status"], dict):
                status_ = systemState_["status"]

                if "mainStatus" in systemState_ and isinstance(status_["mainStatus"], str):
                    try:
                        system_data.systemState.status.mainStatus = MainStatus(status_["mainStatus"])
                    except ValueError:
                        print(f"Error in incoming JSON, unknown mainStatus received: {status_['mainStatus']}")

                if "exteriorAbsHum" in status_ and isinstance(status_["exteriorAbsHum"], float):
                    system_data.systemState.status.exteriorAbsHum = float(status_["exteriorAbsHum"])

                if "interiorAbsHum" in status_ and isinstance(status_["interiorAbsHum"], float):
                    system_data.systemState.status.interiorAbsHum = float(status_["interiorAbsHum"])

                if "heaterSetpoint" in status_ and isinstance(status_["heaterSetpoint"], float):
                    system_data.systemState.status.heaterSetpoint = float(status_["heaterSetpoint"])

                if "fan" in status_ and isinstance(status_["fan"], str):
                    try:
                        system_data.systemState.status.fan = FanState(status_["fan"])
                    except ValueError:
                        print(f"Error in incoming JSON, unknown mainStatus received: {status_['fan']}")

                if "vents" in status_ and isinstance(status_["vents"], str):
                    try:
                        system_data.systemState.status.vents = VentsState(status_["vents"])
                    except ValueError:
                        print(f"Error in incoming JSON, unknown mainStatus received: {status_['vents']}")

            if "systemConfig" in systemState_ and isinstance(systemState_["systemConfig"], dict):
                systemConfig_ = systemState_["systemConfig"]

                if "targetChamberTemp" in systemConfig_ and isinstance(systemConfig_["targetChamberTemp"], float):
                    system_data.systemState.systemConfig.targetChamberTemp = systemConfig_["targetChamberTemp"]

                if "maxAllowedFilamentTemp" in systemConfig_ and isinstance(
                    systemConfig_["maxAllowedFilamentTemp"], float
                ):
                    system_data.systemState.systemConfig.maxAllowedFilamentTemp = systemConfig_[
                        "maxAllowedFilamentTemp"
                    ]

                if "targetRelHum" in systemConfig_ and isinstance(systemConfig_["targetRelHum"], float):
                    system_data.systemState.systemConfig.targetRelHum = systemConfig_["targetRelHum"]

            if "chamberState" in systemState_ and isinstance(systemState_["chamberState"], dict):
                chamberState_ = systemState_["chamberState"]

                if "chamberTemp" in chamberState_ and isinstance(chamberState_["chamberTemp"], dict):
                    chamberTemp_ = chamberState_["chamberTemp"]

                    if "max" in chamberTemp_ and isinstance(chamberTemp_["max"], float):
                        system_data.systemState.chamberState.chamberTemp.max = chamberTemp_["max"]

                    if "avg" in chamberTemp_ and isinstance(chamberTemp_["avg"], float):
                        system_data.systemState.chamberState.chamberTemp.avg = chamberTemp_["avg"]

                if "chamberHum" in chamberState_ and isinstance(chamberState_["chamberHum"], dict):
                    chamberHum_ = chamberState_["chamberHum"]

                    if "max" in chamberHum_ and isinstance(chamberHum_["max"], float):
                        system_data.systemState.chamberState.chamberHum.max = chamberHum_["max"]

                    if "avg" in chamberHum_ and isinstance(chamberHum_["avg"], float):
                        system_data.systemState.chamberState.chamberHum.avg = chamberHum_["avg"]

            if "ambientState" in systemState_ and isinstance(systemState_["ambientState"], dict):
                ambientState_ = systemState_["ambientState"]

                if "temp" in ambientState_ and isinstance(ambientState_["temp"], float):
                    system_data.systemState.ambientState.temp = ambientState_["temp"]

                if "hum" in ambientState_ and isinstance(ambientState_["hum"], float):
                    system_data.systemState.ambientState.hum = ambientState_["hum"]

            if "filamentState" in systemState_ and isinstance(systemState_["filamentState"], dict):
                filamentState_ = systemState_["filamentState"]

                if "filamentTemp" in filamentState_ and isinstance(filamentState_["filamentTemp"], dict):
                    filamentTemp_ = filamentState_["filamentTemp"]

                    if "max" in filamentTemp_ and isinstance(filamentTemp_["max"], float):
                        system_data.systemState.filamentState.filamentTemp.max = filamentTemp_["max"]

                    if "avg" in filamentTemp_ and isinstance(filamentTemp_["avg"], float):
                        system_data.systemState.filamentState.filamentTemp.avg = filamentTemp_["avg"]

        if "rawSensorTelemetry" in data and isinstance(data["rawSensorTelemetry"], dict):
            rawSensorTelemetry_ = data["rawSensorTelemetry"]

            if "chamber" in rawSensorTelemetry_ and isinstance(rawSensorTelemetry_["chamber"], dict):
                chamber_ = rawSensorTelemetry_["chamber"]

                if "sht31_0_temp" in chamber_ and isinstance(chamber_["sht31_0_temp"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_0_temp = chamber_["sht31_0_temp"]

                if "sht31_0_hum" in chamber_ and isinstance(chamber_["sht31_0_hum"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_0_hum = chamber_["sht31_0_hum"]

                if "sht31_1_temp" in chamber_ and isinstance(chamber_["sht31_1_temp"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_1_temp = chamber_["sht31_1_temp"]

                if "sht31_1_hum" in chamber_ and isinstance(chamber_["sht31_1_hum"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_1_hum = chamber_["sht31_1_hum"]

                if "sht31_2_temp" in chamber_ and isinstance(chamber_["sht31_2_temp"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_2_temp = chamber_["sht31_2_temp"]

                if "sht31_2_hum" in chamber_ and isinstance(chamber_["sht31_2_hum"], float):
                    system_data.rawSensorTelemetry.chamber.sht31_2_hum = chamber_["sht31_2_hum"]

                if "ds18b20_temp" in chamber_ and isinstance(chamber_["ds18b20_temp"], float):
                    system_data.rawSensorTelemetry.chamber.ds18b20_temp = chamber_["ds18b20_temp"]

            if "ambient" in rawSensorTelemetry_ and isinstance(rawSensorTelemetry_["ambient"], dict):
                ambient_ = rawSensorTelemetry_["ambient"]

                if "sht31_3_temp" in ambient_ and isinstance(ambient_["sht31_3_temp"], float):
                    system_data.rawSensorTelemetry.ambient.sht31_3_temp = ambient_["sht31_3_temp"]

                if "sht31_3_hum" in ambient_ and isinstance(ambient_["sht31_3_hum"], float):
                    system_data.rawSensorTelemetry.ambient.sht31_3_hum = ambient_["sht31_3_hum"]

            if "filament" in rawSensorTelemetry_ and isinstance(rawSensorTelemetry_["filament"], dict):
                filament_ = rawSensorTelemetry_["filament"]

                if "mlx90614_0_temp" in filament_ and isinstance(filament_["mlx90614_0_temp"], float):
                    system_data.rawSensorTelemetry.filament.mlx90614_0_temp = filament_["mlx90614_0_temp"]

                if "mlx90614_1_temp" in filament_ and isinstance(filament_["mlx90614_1_temp"], float):
                    system_data.rawSensorTelemetry.filament.mlx90614_1_temp = filament_["mlx90614_1_temp"]

    except json.JSONDecodeError as err:
        print(f"JSON decode error: {err}")
        return None

    # Errors from failing to parse data
    except KeyError as err:
        print(f"JSON data structure error, mapping key not found: {err}")
        return None

    except TypeError as err:
        print(f"JSON data structure error, inappropiate argument type: {err}")
        return None

    except ValueError as err:
        print(f"JSON data structure error, inappropiate argument value: {err}")
        return None


# def parse_outgoing_dryer_json() -> None:


def test_parse_incoming_dryer_json() -> None:
    # Test with various JSON documents

    # Valid JSON
    valid_json = """{
        "systemState": {
            "status": {
                "mainStatus": "DRYING",
                "exteriorAbsHum": 8.5,
                "interiorAbsHum": 12.3,
                "heaterSetpoint": 65.0,
                "fan": "ON",
                "vents": "CLOSED"
            },
            "systemConfig": {
                "targetChamberTemp": 60.0,
                "maxAllowedFilamentTemp": 80.0,
                "targetRelHum": 15.0
            },
            "chamberState": {
                "chamberTemp": {"max": 61.2, "avg": 60.5},
                "chamberHum": {"max": 16.5, "avg": 15.8}
            },
            "ambientState": {"temp": 22.5, "hum": 45.0},
            "filamentState": {"filamentTemp": {"max": 72.3, "avg": 71.8}}
        },
        "rawSensorTelemetry": {
            "chamber": {
                "sht31_0_temp": 60.2, "sht31_0_hum": 15.5,
                "sht31_1_temp": 60.8, "sht31_1_hum": 16.0,
                "sht31_2_temp": 60.5, "sht31_2_hum": 15.9,
                "ds18b20_temp": 60.3
            },
            "ambient": {"sht31_3_temp": 22.5, "sht31_3_hum": 45.0},
            "filament": {"mlx90614_0_temp": 71.5, "mlx90614_1_temp": 72.1}
        }
    }"""

    # JSON with wrong types (should be ignored/skipped)
    wrong_types_json = """{
        "systemState": {
            "status": {
                "mainStatus": 123,
                "exteriorAbsHum": "not a number",
                "heaterSetpoint": "wrong type"
            }
        }
    }"""

    print("=== Processing Valid JSON ===")
    parse_incoming_dryer_json(valid_json)
    print(f"Status: {system_data.systemState.status.mainStatus.value}")
    print(f"Exterior Abs Hum: {system_data.systemState.status.exteriorAbsHum}")
    print(f"Heater Setpoint: {system_data.systemState.status.heaterSetpoint}")

    print("\n=== Processing JSON with Wrong Types ===")
    parse_incoming_dryer_json(wrong_types_json)
    print(f"Status still: {system_data.systemState.status.mainStatus.value} (unchanged because type was wrong)")
    print(f"Exterior Abs Hum still: {system_data.systemState.status.exteriorAbsHum} (unchanged)")


if __name__ == "__main__":
    test_parse_incoming_dryer_json()
