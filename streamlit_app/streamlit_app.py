import json
from pathlib import Path

import pandas as pd
import streamlit as st
import altair as alt

DATA_FILE = Path(__file__).resolve().parents[1] / "output" / "ac2r_analysis" / "summary.json"

@st.cache_data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def main() -> None:
    st.title("Sincera Metrics Summary")
    data = load_data()

    metrics = ["a2cr", "total_supply_paths", "avg_page_weight"]

    for metric in metrics:
        rows = []
        for seller, stats in data.items():
            network = (
                seller.replace("sellers_", "")
                .replace("_percentiles", "")
                .replace("_", " ")
                .title()
            )

            mstats = stats.get(metric, {})
            rows.append(
                {
                    "network": network,
                    "n": mstats.get("n", 0),
                    "p25": mstats.get("p25"),
                    "p50": mstats.get("p50"),
                    "p75": mstats.get("p75"),
                }
            )

        df = pd.DataFrame(rows)
        st.subheader(metric.replace("_", " ").title())

        base = alt.Chart(df).encode(x=alt.X("network:N", title="Network"))
        rule = base.mark_rule().encode(y="p25:Q", y2="p75:Q")

        long_df = df.melt(
            id_vars=["network"],
            value_vars=["p25", "p50", "p75"],
            var_name="percentile",
            value_name="value",
        )

        points = (
            alt.Chart(long_df)
            .mark_point(filled=True, size=100)
            .encode(
                x="network:N",
                y=alt.Y("value:Q", title=metric.replace("_", " ").title()),
                color="percentile:N",
                shape="percentile:N",
            )
        )

        st.altair_chart(rule + points, use_container_width=True)

    # Display the sample size table once using the first metric
    rows = []
    for seller, stats in data.items():
        network = (
            seller.replace("sellers_", "")
            .replace("_percentiles", "")
            .replace("_", " ")
            .title()
        )
        mstats = stats.get(metrics[0], {})
        rows.append({"network": network, "n": mstats.get("n", 0)})

    df = pd.DataFrame(rows)
    st.subheader("Number of domains used for each network")
    st.table(df.set_index("network"))

if __name__ == "__main__":
    main()
