import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).resolve().parents[1] / "output" / "ac2r_analysis" / "summary.json"

@st.cache_data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def main() -> None:
    st.title("A2CR Summary")
    data = load_data()
    for seller, stats in data.items():
        st.subheader(seller.replace("_", " ").title())
        st.metric("Number of domains", stats["n"])
        df = pd.DataFrame(
            {
                "percentile": ["p25", "p50", "p75"],
                "value": [stats["p25"], stats["p50"], stats["p75"],],
            }
        ).set_index("percentile")
        st.bar_chart(df)

if __name__ == "__main__":
    main()
