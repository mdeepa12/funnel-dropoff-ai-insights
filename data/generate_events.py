import argparse
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/events.csv")
    parser.add_argument("--users", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    np.random.seed(args.seed)

    users = args.users
    start = pd.Timestamp("2024-01-01")
    end = pd.Timestamp("2024-12-31")

    devices = ["mobile", "web"]
    regions = ["NA", "EU", "APAC"]
    device_p = [0.65, 0.35]
    region_p = [0.50, 0.25, 0.25]

    # Base step probabilities (realistic drop-offs)
    # visit -> signup -> product_view -> add_to_cart -> purchase
    base = {
        "signup": 0.35,
        "product_view": 0.70,
        "add_to_cart": 0.28,
        "purchase": 0.55
    }

    # Segment effects (mobile + APAC slightly worse add_to_cart, example)
    def adjust_probs(device, region):
        p = base.copy()
        if device == "mobile":
            p["add_to_cart"] *= 0.90
        if region == "APAC":
            p["add_to_cart"] *= 0.92
        if region == "NA":
            p["purchase"] *= 1.03
        return p

    rows = []
    for user_id in range(1, users + 1):
        device = np.random.choice(devices, p=device_p)
        region = np.random.choice(regions, p=region_p)

        # random first visit date
        t0 = start + pd.to_timedelta(np.random.randint(0, (end - start).days + 1), unit="D")
        # visit always happens
        rows.append((user_id, "visit", t0 + pd.to_timedelta(np.random.randint(0, 3600), unit="s"), device, region))

        p = adjust_probs(device, region)

        # signup
        if np.random.rand() < p["signup"]:
            t1 = t0 + pd.to_timedelta(np.random.randint(1, 48), unit="h")
            rows.append((user_id, "signup", t1, device, region))
        else:
            continue

        # product_view
        if np.random.rand() < p["product_view"]:
            t2 = t1 + pd.to_timedelta(np.random.randint(1, 24), unit="h")
            rows.append((user_id, "product_view", t2, device, region))
        else:
            continue

        # add_to_cart
        if np.random.rand() < p["add_to_cart"]:
            t3 = t2 + pd.to_timedelta(np.random.randint(1, 12), unit="h")
            rows.append((user_id, "add_to_cart", t3, device, region))
        else:
            continue

        # purchase
        if np.random.rand() < p["purchase"]:
            t4 = t3 + pd.to_timedelta(np.random.randint(1, 12), unit="h")
            rows.append((user_id, "purchase", t4, device, region))

    df = pd.DataFrame(rows, columns=["user_id", "event_name", "event_time", "device", "region"])
    df["event_time"] = pd.to_datetime(df["event_time"])
    df = df.sort_values(["event_time", "user_id"]).reset_index(drop=True)

    df.to_csv(args.out, index=False)
    print(f"Saved {len(df):,} rows to {args.out}")

if __name__ == "__main__":
    main()

