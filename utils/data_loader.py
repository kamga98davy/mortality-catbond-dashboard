"""Data loading and preprocessing for the mortality CAT bond dashboard."""
from __future__ import annotations

import json
import warnings
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA_DIR = Path(__file__).parent.parent / "data"

warnings.filterwarnings("ignore", category=UserWarning)


# ── Excel loaders ──────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def load_mortality_raw() -> pd.DataFrame | None:
    path = DATA_DIR / "mortalite_final.xlsx"
    if not path.exists():
        return None
    df = pd.read_excel(path, sheet_name="base_complet")
    df.columns = df.columns.str.strip()
    df = df.sort_values(["Year", "Semaine"]).reset_index(drop=True)
    df["Date"] = pd.to_datetime(
        df["Year"].astype(str) + "-W" + df["Semaine"].astype(str).str.zfill(2) + "-1",
        format="%Y-W%W-%w",
        errors="coerce",
    )
    df["Taux_mortalite"] = df["deces"] / df["Pop_hebdomadaire"] * 1000
    return df


@lru_cache(maxsize=1)
def load_mortality() -> pd.DataFrame | None:
    """Load mortality data + fit GLM Poisson + compute mu_t."""
    df = load_mortality_raw()
    if df is None:
        return None
    df = df.copy()
    n = len(df)
    df["t"] = np.arange(1, n + 1)
    df["log_pop"] = np.log(df["Pop_hebdomadaire"])
    for k in (1, 2):
        df[f"sin{k}"] = np.sin(2 * np.pi * k * df["Semaine"] / 52)
        df[f"cos{k}"] = np.cos(2 * np.pi * k * df["Semaine"] / 52)

    X = sm.add_constant(df[["t", "sin1", "cos1", "sin2", "cos2"]])
    glm = sm.GLM(
        df["deces"], X,
        family=sm.families.Poisson(),
        offset=df["log_pop"],
    ).fit(disp=False)

    df["deces_attendus"] = glm.fittedvalues
    df["mu_t"] = (df["deces"] - df["deces_attendus"]) / df["Pop_hebdomadaire"] * 100
    df["periode"] = np.where(df["Year"] < 2020, "Pré-COVID", "Post-COVID")
    return df


@lru_cache(maxsize=1)
def load_interest_rate() -> pd.DataFrame | None:
    path = DATA_DIR / "taux_journalier.xlsx"
    if not path.exists():
        return None
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"clot": "taux_clot"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).copy()
    df["Year"] = df["date"].dt.year
    df["Semaine"] = df["date"].dt.isocalendar().week.astype(int)
    df = df[(df["Year"] >= 2016) & (df["Year"] <= 2024)]
    df = df[~((df["Year"] == 2020) & (df["Semaine"] == 53))]
    taux_hebdo = (
        df.sort_values("date")
          .groupby(["Year", "Semaine"], as_index=False)
          .last()
    )
    taux_hebdo["Date"] = pd.to_datetime(
        taux_hebdo["Year"].astype(str) + "-W"
        + taux_hebdo["Semaine"].astype(str).str.zfill(2) + "-1",
        format="%Y-W%W-%w",
        errors="coerce",
    )
    return taux_hebdo[["Year", "Semaine", "Date", "taux_clot"]]


# ── JSON loaders ───────────────────────────────────────────────────────────────

def _load_json(filename: str) -> dict | None:
    path = DATA_DIR / filename
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_params_postC() -> dict | None:
    return _load_json("params_postC.json")


@lru_cache(maxsize=1)
def load_params_preC() -> dict | None:
    return _load_json("params_preC.json")


@lru_cache(maxsize=1)
def load_seuils() -> dict | None:
    return _load_json("seuils.json")


@lru_cache(maxsize=1)
def load_mpr() -> dict | None:
    return _load_json("mpr.json")


# ── CSV loaders ────────────────────────────────────────────────────────────────

@lru_cache(maxsize=2)
def load_mcmc_summary(period: str = "postC") -> pd.DataFrame | None:
    path = DATA_DIR / f"mcmc_summary_{period}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@lru_cache(maxsize=2)
def load_mcmc_chains(period: str = "postC") -> pd.DataFrame | None:
    path = DATA_DIR / f"mcmc_chains_{period}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@lru_cache(maxsize=1)
def load_sensitivity() -> pd.DataFrame | None:
    path = DATA_DIR / "sensitivity.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@lru_cache(maxsize=1)
def load_exceedance() -> pd.DataFrame | None:
    path = DATA_DIR / "exceedance.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@lru_cache(maxsize=1)
def load_etats() -> pd.DataFrame | None:
    path = DATA_DIR / "etats_calibration.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


# ── Descriptive statistics ─────────────────────────────────────────────────────

def compute_stats(series: pd.Series) -> dict:
    from scipy.stats import skew, kurtosis
    return {
        "N": int(len(series)),
        "Moyenne": round(float(series.mean()), 4),
        "Médiane": round(float(series.median()), 4),
        "Écart-type": round(float(series.std()), 4),
        "Min": round(float(series.min()), 4),
        "Max": round(float(series.max()), 4),
        "Q1": round(float(series.quantile(0.25)), 4),
        "Q3": round(float(series.quantile(0.75)), 4),
        "Skewness": round(float(skew(series.dropna())), 4),
        "Kurtosis": round(float(kurtosis(series.dropna())), 4),
        "% > 0": round(float((series > 0).mean() * 100), 2),
    }


def corr_instantanee(p: dict) -> float:
    """Compute instantaneous correlation corr(dr_t, dmu_t) from Li et al. eq. 2.10."""
    num = (p["rho1"] * p["sigma1"] * p["sigma2"]
           + p["lambda"] * (p["rho2"] * p["phi1"] * p["phi2"] + p["v1"] * p["v2"]))
    den = (np.sqrt(p["sigma1"]**2 + p["lambda"] * (p["phi1"]**2 + p["v1"]**2))
           * np.sqrt(p["sigma2"]**2 + p["lambda"] * (p["phi2"]**2 + p["v2"]**2)))
    return num / den if den != 0 else float("nan")
