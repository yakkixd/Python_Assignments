from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = float(kwh)

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, timestamp, kwh):
        self.meter_readings.append(MeterReading(timestamp, kwh))

    def total(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        return f"{self.name}: {self.total():.2f} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_df(self, df):
        for row in df.itertuples(index=False):
            b = self.get_or_create(row.building)
            b.add_reading(row.timestamp, row.kwh)

    def total_campus(self):
        return sum(b.total() for b in self.buildings.values())

    def top_building(self):
        if not self.buildings:
            return "", 0.0
        b = max(self.buildings.values(), key=lambda x: x.total())
        return b.name, b.total()

    def reports(self):
        return [b.generate_report() for b in self.buildings.values()]

def load_data():
    dfs = []
    if not DATA_DIR.exists():
        return pd.DataFrame()
    for f in DATA_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(f, on_bad_lines="skip")
        except Exception:
            continue
        if "timestamp" not in df.columns or "kwh" not in df.columns:
            continue
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
        df["building"] = f.stem
        df["month"] = df["timestamp"].dt.to_period("M").astype(str)
        df = df.dropna(subset=["timestamp", "kwh"])
        dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
    return df.sort_values("timestamp").reset_index(drop=True)

def daily_totals(df):
    idx = df.set_index("timestamp")
    return idx.groupby("building")["kwh"].resample("D").sum().reset_index(name="daily_kwh")

def weekly_totals(df):
    idx = df.set_index("timestamp")
    return idx.groupby("building")["kwh"].resample("W").sum().reset_index(name="weekly_kwh")

def building_summary(df):
    s = df.groupby("building")["kwh"].agg(["sum", "mean", "min", "max"]).reset_index()
    return s.rename(columns={"sum": "total_kwh", "mean": "mean_kwh", "min": "min_kwh", "max": "max_kwh"})

def create_dashboard(df, daily, weekly):
    weekly_avg = weekly.groupby("building")["weekly_kwh"].mean().reset_index()
    peak_idx = df.groupby("building")["kwh"].idxmax()
    peak_df = df.loc[peak_idx, ["timestamp", "kwh", "building"]]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax1, ax2 = axes[0]
    ax3 = axes[1, 0]
    axes[1, 1].axis("off")

    for b, g in daily.groupby("building"):
        ax1.plot(g["timestamp"], g["daily_kwh"], marker="o", label=b)
    ax1.set_title("Daily Consumption")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar(weekly_avg["building"], weekly_avg["weekly_kwh"])
    ax2.set_title("Avg Weekly Consumption")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("kWh")
    ax2.tick_params(axis="x", rotation=20)

    for b, g in peak_df.groupby("building"):
        ax3.scatter(g["timestamp"], g["kwh"], label=b)
    ax3.set_title("Peak-Hour Consumption")
    ax3.set_xlabel("Timestamp")
    ax3.set_ylabel("kWh")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    fig.suptitle("Campus Energy-Use Dashboard")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUTPUT_DIR / "dashboard.png", dpi=150)
    plt.close(fig)

def write_outputs(df, summary, mgr, daily, weekly):
    df.to_csv(OUTPUT_DIR / "cleaned_energy_data.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "building_summary.csv", index=False)

    total_campus = mgr.total_campus()
    top_name, top_val = mgr.top_building()

    peak_idx = df["kwh"].idxmax()
    peak_row = df.loc[peak_idx]
    peak_time = peak_row["timestamp"]
    peak_building = peak_row["building"]
    peak_kwh = peak_row["kwh"]

    idx = df.set_index("timestamp")
    weekday_stats = idx["kwh"].groupby(idx.index.day_name()).mean().sort_values(ascending=False)

    w_tot = idx["kwh"].resample("W").sum()
    w_mean = w_tot.mean()
    w_max = w_tot.max()

    lines = []
    lines.append("=== Campus Energy Executive Summary ===")
    lines.append(f"Total campus consumption: {total_campus:.2f} kWh")
    lines.append(f"Highest-consuming building: {top_name} ({top_val:.2f} kWh)")
    lines.append(f"Overall peak load: {peak_kwh:.2f} kWh at {peak_time} in {peak_building}")
    lines.append("")
    lines.append("Average consumption by weekday:")
    for d, v in weekday_stats.items():
        lines.append(f"  {d}: {v:.2f} kWh")
    lines.append("")
    lines.append(f"Average weekly total: {w_mean:.2f} kWh")
    lines.append(f"Maximum weekly total: {w_max:.2f} kWh")
    lines.append("")
    lines.append("Per-building totals:")
    for r in mgr.reports():
        lines.append("  " + r)

    text_path = OUTPUT_DIR / "summary.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))

def main():
    df = load_data()
    if df.empty:
        print("No valid data found in 'data/'")
        return
    daily = daily_totals(df)
    weekly = weekly_totals(df)
    summary = building_summary(df)
    mgr = BuildingManager()
    mgr.load_from_df(df)
    create_dashboard(df, daily, weekly)
    write_outputs(df, summary, mgr, daily, weekly)
    print("Outputs saved in 'output/'")

if __name__ == "__main__":
    main()
