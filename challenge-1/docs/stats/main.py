import json

import pandas as pd


def compute_transmission_power():
    file_path = "../transmission_power.csv"
    try:
        df = pd.read_csv(file_path)
        if "Data" in df.columns:
            filtered_avg = {
                "tx_19dBm": df["Data"][df["Data"] >= 1150].mean(),
                "tx_2dBm": df["Data"][(df["Data"] >= 750) & (df["Data"] < 850)].mean(),
            }
        else:
            filtered_avg = None
    except Exception as e:
        print(f"Error reading sensor CSV: {e}")
        filtered_avg = None

    return filtered_avg


def compute_sensor_read():
    file_path = "../sensor_read.csv"
    try:
        df = pd.read_csv(file_path)
        if "Data" in df.columns:
            filtered_avg = {
                "sensor_reading": df["Data"][df["Data"] > 460].mean(),
            }
        else:
            filtered_avg = None
    except Exception as e:
        print(f"Error reading sensor CSV: {e}")
        filtered_avg = None

    return filtered_avg


def compute_deep_sleep():
    file_path = "../deep_sleep.csv"
    try:
        df = pd.read_csv(file_path)
        if "Data" in df.columns:
            filtered_avg = {
                "deep_sleep": df["Data"][df["Data"] < 100].mean(),
                "idle": df["Data"][(df["Data"] >= 300) & (df["Data"] <= 320)].mean(),
                "wifi_on": df["Data"][df["Data"] > 750].mean(),
            }
        else:
            filtered_avg = None
    except Exception as e:
        print(f"Error reading deep sleep CSV: {e}")
        filtered_avg = None

    return filtered_avg


if __name__ == "__main__":
    results = {
        "transmission_power": compute_transmission_power(),
        "sensor_read": compute_sensor_read(),
        "deep_sleep": compute_deep_sleep(),
    }

    print("Final results:")
    print(json.dumps(results, indent=4))
