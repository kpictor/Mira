"""BLS public data API v2 adapter -> canonical ``macro_series`` (keyless).

Official macro statistics (fact / L2). The keyless GET returns the most recent
~3 years for a series; FRED/BEA (keyed) are deferred to a later phase. The full
series is returned as a bulk ``series``; the latest observation becomes the
single evidence-log claim.
"""

from __future__ import annotations

import datetime as _dt
from typing import Optional

from .. import net
from ..canonical import POSTURES, CanonicalRecord, FetchResult

SERIES_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/{series_id}"
SERIES_COLUMNS = ["series_id", "year", "period", "period_name", "value"]


def fetch_macro_series(
    series_id: str,
    *,
    as_of: Optional[str] = None,
    market_scope: str = "US",
) -> FetchResult:
    as_of = as_of or _dt.date.today().isoformat()
    url = SERIES_URL.format(series_id=series_id)
    payload = net.get_json(url)
    if payload.get("status") != "REQUEST_SUCCEEDED":
        msg = "; ".join(payload.get("message", [])) or payload.get("status", "unknown error")
        raise net.FetchError(f"source_gap: BLS request not processed for {series_id}: {msg}")

    series_list = payload.get("Results", {}).get("series", [])
    points = series_list[0].get("data", []) if series_list else []
    if not points:
        raise net.FetchError(f"source_gap: no BLS observations for {series_id}")

    rows = [
        {"series_id": series_id, "year": d.get("year"), "period": d.get("period"),
         "period_name": d.get("periodName"), "value": d.get("value")}
        for d in points
    ]
    latest = points[0]  # BLS returns most-recent-first
    rec = CanonicalRecord(
        family="macro_series", research_object=series_id, market_scope=market_scope,
        metric=series_id, value=_num(latest.get("value")), unit="value",
        period=f"{latest.get('year')}-{latest.get('period')}", period_type="calendar_period",
        as_of_date=as_of, source_date=as_of, posture=POSTURES["bls"], url_or_path=url,
        claim_text=f"BLS {series_id} {latest.get('periodName')} {latest.get('year')} = {latest.get('value')}",
        provenance={"series_id": series_id, "period_name": latest.get("periodName")},
    )
    series = {"name": f"macro_series-{series_id}", "columns": SERIES_COLUMNS, "rows": rows}
    return FetchResult([rec], series=series)


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return value
