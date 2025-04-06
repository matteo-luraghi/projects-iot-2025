import json
import pandas as pd

def compute_transmission_power():
    df = pd.read_csv("transmission_power.csv")
    transmission_powers = {
        "tx_19dBm": df["Data"][df["Data"] >= 1150].mean(),
        "tx_2dBm": df["Data"][(df["Data"] >= 750) & (df["Data"] < 850)].mean(),
    }
    return transmission_powers

def compute_sensor_read():
    df = pd.read_csv("sensor_read.csv")
    sensor_read_power = {
        "sensor_reading": df["Data"][df["Data"] > 460].mean(),
    }
    return sensor_read_power 

def compute_deep_sleep():
    df = pd.read_csv("deep_sleep.csv")
    deep_sleep_powers = {
        "deep_sleep": df["Data"][df["Data"] < 100].mean(),
        "idle": df["Data"][(df["Data"] >= 300) & (df["Data"] <= 320)].mean(),
        "wifi_on": df["Data"][df["Data"] > 750].mean(),
    }
    return deep_sleep_powers


if __name__ == "__main__":
    results = {
        "transmission_power": compute_transmission_power(),
        "sensor_read_power": compute_sensor_read(),
        "deep_sleep_power": compute_deep_sleep(),
    }

    print(json.dumps(results, indent=4))