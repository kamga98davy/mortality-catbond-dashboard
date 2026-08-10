# Belgian Mortality CAT Bond Dashboard

Interactive Streamlit dashboard for the thesis:
**"Pricing Extreme Mortality Risk in the Wake of the COVID-19 Pandemic — Application to Belgium"**

Replication of Li, Liu, Tang & Yuan (2023, *Insurance: Mathematics and Economics*).

## Live Demo

> Deploy link will appear here after Streamlit Cloud deployment.

## Sections

| Page | Content |
|:---|:---|
| Home | KPIs, context, 3 scenarios |
| Données | Weekly mortality, GLM Poisson, μₜ, EURIBOR |
| Modèle AJD | Bivariate SDE specification, P→Q measure change |
| Calibration MCMC | Metropolis-Hastings results, ESS, trace plots |
| Monte Carlo | Exceedance curve, thresholds a_BE/b_BE |
| Pricing | MPR vector ζ, scenarios S1/S2/S3 |
| Sensibilité | Interactive MPR sliders, price sensitivity |

## Quick Start (Local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Setup (required before first run)

**Step 1 — Copy Excel files**

Copy these files from your R project to `data/`:
```
mortalite_final.xlsx
taux_journalier.xlsx
```

**Step 2 — Export R results**

Open R/RStudio and run:
```r
source("export_for_streamlit.R")
```

This generates in `data/`:
- `mcmc_summary_postC.csv` — MCMC parameter estimates (post-COVID)
- `mcmc_summary_preC.csv` — MCMC parameter estimates (pre-COVID)
- `mcmc_chains_postC.csv` — Thinned MCMC chains (1 000 samples)
- `params_postC.json` / `params_preC.json` — Parameter means
- `seuils.json` — Attachment/exhaustion thresholds
- `exceedance.csv` — Exceedance curve data points
- `mpr.json` — Market Price of Risk vector ζ
- `sensitivity.csv` — Sensitivity analysis results
- `etats_calibration.csv` — Quarterly calibration states (2011-2015)

## GitHub Deployment

See deployment instructions below.

## Tech Stack

- **Python** 3.10+
- **Streamlit** 1.36+
- **Plotly** — interactive charts
- **statsmodels** — GLM Poisson (live computation)
- **scipy** — interpolation for sensitivity sliders

## Reference

Li, Z., Liu, X., Tang, Q., & Yuan, Z. (2023).
Pricing extreme mortality risk in the wake of the COVID-19 pandemic.
*Insurance: Mathematics and Economics*, 85, 84–106.
DOI: 10.1016/j.insmatheco.2022.09.006
