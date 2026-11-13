"""Read-only unemployment dashboard backed by PostgreSQL."""
import pandas as pd
import psycopg
from psycopg.rows import dict_row
import streamlit as st

st.set_page_config(page_title="SA Economic Dashboard", layout="wide")
st.title("South Africa: unemployment")
st.caption("World Bank · Modeled ILO estimate · Annual data · % of total labor force")

@st.cache_data(ttl=300)
def load_data():
    settings = dict(st.secrets["database"])
    with psycopg.connect(**settings, connect_timeout=10, row_factory=dict_row) as conn:
        conn.execute("SET TRANSACTION READ ONLY")
        records = conn.execute(
            """SELECT year, unemployment_pct, retrieved_at_utc
               FROM public.unemployment_observations
               WHERE country_code = %s AND indicator_code = %s
               ORDER BY year""",
            ("ZAF", "SL.UEM.TOTL.ZS"),
        ).fetchall()
    frame = pd.DataFrame(records)
    if not frame.empty:
        frame["unemployment_pct"] = pd.to_numeric(frame["unemployment_pct"])
        frame["retrieved_at_utc"] = pd.to_datetime(frame["retrieved_at_utc"], utc=True)
    return frame

if st.sidebar.button("Reload database data"):
    load_data.clear()

try:
    data = load_data()
except Exception:
    st.error("Could not load data. Check the local database and secrets configuration.")
    st.stop()

if data.empty or data["unemployment_pct"].notna().sum() == 0:
    st.warning("No available observations. Run the ingestion and SQL import first.")
    st.stop()

valid = data.dropna(subset=["unemployment_pct"])
low, high = int(valid.year.min()), int(valid.year.max())
years = st.sidebar.slider("Year range", low, high, (low, high)) if low < high else (low, high)
selected = data[data.year.between(*years)].copy()
available = selected.dropna(subset=["unemployment_pct"])
if available.empty:
    st.warning("No available values in this range.")
    st.stop()

latest = available.iloc[-1]
previous = data.loc[data.year == int(latest.year) - 1, "unemployment_pct"]
delta = None
if not previous.empty and pd.notna(previous.iloc[0]):
    delta = f"{float(latest.unemployment_pct - previous.iloc[0]):+.3f} pp vs prior year"

a, b, c, d = st.columns(4)
a.metric(f"Latest selected year: {int(latest.year)}", f"{latest.unemployment_pct:.3f}%", delta=delta, delta_color="inverse")
peak = available.loc[available.unemployment_pct.idxmax()]
b.metric("Highest in selected range", f"{peak.unemployment_pct:.3f}%", f"Year {int(peak.year)}", delta_color="off")
c.metric("Available annual values", len(available))
average_rate = available["unemployment_pct"].mean()
d.metric("Average annual rate", f"{average_rate:.3f}%")
st.caption("Average: unweighted mean of available annual rates within the selected year range.")
st.subheader("Annual unemployment rate")
st.line_chart(selected.set_index("year")[["unemployment_pct"]], y_label="Unemployment (%)", x_label="Year")

st.subheader("Year-over-year change")
indexed = data.set_index("year")["unemployment_pct"]
selected["change_pp"] = [
    value - indexed.get(year - 1, float("nan"))
    for year, value in zip(selected.year, selected.unemployment_pct)
]
st.bar_chart(selected.set_index("year")[["change_pp"]], y_label="Percentage points", x_label="Year")

st.subheader("Data coverage")
st.write(f"Full dataset: {len(data)} returned years; {len(valid)} available; {int(data.unemployment_pct.isna().sum())} missing.")
st.caption(f"Latest retrieval in database: {data.retrieved_at_utc.max().isoformat()}. Reloads are cached for up to five minutes.")
with st.expander("Inspect and download selected rows"):
    st.dataframe(selected, hide_index=True)
    st.download_button("Download selected CSV", selected.to_csv(index=False), "selected_unemployment.csv", "text/csv")

st.info("Missing observations are not zero. Modeled ILO estimates may differ from national survey figures and may be revised. These charts describe changes; they do not establish causes. pp = percentage points.")
st.markdown("[Source and indicator definition](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=ZA)")
