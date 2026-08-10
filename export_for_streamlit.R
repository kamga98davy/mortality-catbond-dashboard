# =============================================================================
# export_for_streamlit.R
# Lance ce script UNE FOIS depuis R/RStudio pour exporter les résultats RDS
# vers des fichiers CSV/JSON lisibles par le dashboard Streamlit.
#
# Usage : setwd("C:/Users/LGC/Desktop/Memoire/base_donnée")
#         source("../mortality_dashboard/export_for_streamlit.R")
# =============================================================================

library(jsonlite)
library(dplyr)

base_path   <- "C:/Users/LGC/Desktop/Memoire/base_donnée"
export_path <- "C:/Users/LGC/Desktop/Memoire/mortality_dashboard/data"
dir.create(export_path, showWarnings = FALSE, recursive = TRUE)

cat("=== Export pour Streamlit ===\n\n")

# ── 1. Copier les fichiers Excel ─────────────────────────────────────────────
for (f in c("mortalite_final.xlsx", "taux_journalier.xlsx", "BEL 2013_2017.xlsx")) {
  src <- file.path(base_path, f)
  dst <- file.path(export_path, f)
  if (file.exists(src)) {
    file.copy(src, dst, overwrite = TRUE)
    cat(sprintf("  Copié : %s\n", f))
  } else {
    cat(sprintf("  MANQUANT : %s\n", f))
  }
}

# ── 2. MCMC post-COVID (2017–2022) ───────────────────────────────────────────
cat("\n[1/6] Export MCMC post-COVID…\n")
obj_v5 <- readRDS(file.path(base_path, "modele_corrige_v5.rds"))
nat5   <- obj_v5$nat

# Renommer colonnes R → Python
nat5 <- nat5 %>% rename_with(~case_when(
  . == "s1"  ~ "sigma1",
  . == "s2"  ~ "sigma2",
  . == "lam" ~ "lambda",
  TRUE        ~ .
))

# Résumé (mean, sd, CI 95%)
mcmc_summary <- data.frame(
  param       = colnames(nat5),
  label       = c("m₁","d₁","m₂","d₂","σ₁","σ₂","ρ₁","λ","ν₁","ν₂","φ₁","φ₂","ρ₂"),
  description = c(
    "Drift moyen taux","Vitesse mean-rev. taux","Drift moyen mort.",
    "Vitesse mean-rev. mort.","Diffusion taux","Diffusion mort.",
    "Corrélation brownienne","Fréquence sauts","Saut moyen taux",
    "Saut moyen mort.","Std saut taux","Std saut mort.","Corr. sauts"),
  mean   = sapply(nat5, mean),
  sd     = sapply(nat5, sd),
  ci_025 = sapply(nat5, quantile, 0.025),
  ci_975 = sapply(nat5, quantile, 0.975),
  stringsAsFactors = FALSE
)

# ESS
if (requireNamespace("coda", quietly = TRUE)) {
  mcmc_summary$ESS <- sapply(nat5, function(x) as.numeric(coda::effectiveSize(x)))
} else {
  mcmc_summary$ESS <- NA_real_
}

write.csv(mcmc_summary, file.path(export_path, "mcmc_summary_postC.csv"), row.names = FALSE)

# Chains thinned à 1 000 itérations
thin_idx <- round(seq(1, nrow(nat5), length.out = min(1000, nrow(nat5))))
write.csv(nat5[thin_idx, ], file.path(export_path, "mcmc_chains_postC.csv"), row.names = FALSE)

# params_postC.json (moyennes)
params_postC <- as.list(colMeans(nat5))
write_json(params_postC, file.path(export_path, "params_postC.json"), auto_unbox = TRUE, digits = 8)
cat("  Done: mcmc_summary_postC.csv, mcmc_chains_postC.csv, params_postC.json\n")

# ── 3. MCMC pré-COVID (2017–2019) ────────────────────────────────────────────
cat("[2/6] Export MCMC pré-COVID…\n")
obj_v5_1719 <- readRDS(file.path(base_path, "modele_corrige_v5_2017_2019.rds"))
nat5_1719   <- obj_v5_1719$nat

nat5_1719 <- nat5_1719 %>% rename_with(~case_when(
  . == "s1"  ~ "sigma1",
  . == "s2"  ~ "sigma2",
  . == "lam" ~ "lambda",
  TRUE        ~ .
))

mcmc_summary_pre <- data.frame(
  param  = colnames(nat5_1719),
  mean   = sapply(nat5_1719, mean),
  sd     = sapply(nat5_1719, sd),
  ci_025 = sapply(nat5_1719, quantile, 0.025),
  ci_975 = sapply(nat5_1719, quantile, 0.975),
  stringsAsFactors = FALSE
)
if (requireNamespace("coda", quietly = TRUE)) {
  mcmc_summary_pre$ESS <- sapply(nat5_1719, function(x) as.numeric(coda::effectiveSize(x)))
} else {
  mcmc_summary_pre$ESS <- NA_real_
}

write.csv(mcmc_summary_pre, file.path(export_path, "mcmc_summary_preC.csv"), row.names = FALSE)

thin_idx2 <- round(seq(1, nrow(nat5_1719), length.out = min(1000, nrow(nat5_1719))))
write.csv(nat5_1719[thin_idx2, ], file.path(export_path, "mcmc_chains_preC.csv"), row.names = FALSE)

params_preC <- as.list(colMeans(nat5_1719))
write_json(params_preC, file.path(export_path, "params_preC.json"), auto_unbox = TRUE, digits = 8)
cat("  Done: mcmc_summary_preC.csv, mcmc_chains_preC.csv, params_preC.json\n")

# ── 4. Seuils & courbe d'exceedance ──────────────────────────────────────────
cat("[3/6] Export seuils et courbe d'exceedance…\n")
res_seuils <- readRDS(file.path(base_path, "seuils_BE.rds"))
a_BE <- res_seuils$a_BE
b_BE <- res_seuils$b_BE
mu_star <- res_seuils$mu_star

# Seuils pré-COVID (s'ils existent)
a_BE_preC <- NULL; b_BE_preC <- NULL
map_result <- tryCatch(readRDS(file.path(base_path, "map_result_v5.rds")), error = function(e) NULL)

seuils_export <- list(
  a_BE  = a_BE, b_BE = b_BE,
  p_att = 1.16, p_exh = 0.74,
  N_sim = length(mu_star), T_bond = res_seuils$T_bond
)

# Ajouter seuils pré-COVID si disponibles
if (!is.null(res_seuils$a_BE_preC)) {
  seuils_export$a_BE_preC <- res_seuils$a_BE_preC
  seuils_export$b_BE_preC <- res_seuils$b_BE_preC
}

write_json(seuils_export, file.path(export_path, "seuils.json"), auto_unbox = TRUE, digits = 8)

# Courbe d'exceedance (3 000 points entre P98 et P99.99)
seuil_bas <- quantile(mu_star, 0.98)
seuil_hau <- quantile(mu_star, 0.9999)
seuils_seq <- seq(seuil_bas, seuil_hau, length.out = 3000)
prob_exc   <- sapply(seuils_seq, function(s) mean(mu_star > s)) * 100
df_exc <- data.frame(seuil = seuils_seq, prob_pct = prob_exc)
write.csv(df_exc, file.path(export_path, "exceedance.csv"), row.names = FALSE)
cat("  Done: seuils.json, exceedance.csv\n")

# ── 5. MPR & scénarios ───────────────────────────────────────────────────────
cat("[4/6] Export MPR et scénarios…\n")
res_MPR <- readRDS(file.path(base_path, "resultats_MPR_1.rds"))
zeta_hat <- res_MPR$zeta_hat

mpr_export <- list(
  gamma1 = zeta_hat[1], gamma2 = zeta_hat[2],
  kappa1 = zeta_hat[3], kappa2 = zeta_hat[4],
  chi    = zeta_hat[5],
  SSE    = res_MPR$SSE_hat,
  P0_S1  = 100.0
)

# Scénario S3
res_S3 <- tryCatch(readRDS(file.path(base_path, "resultats_S3.rds")), error = function(e) NULL)
if (!is.null(res_S3)) {
  zeta_S3 <- res_S3$zeta_S3
  mpr_export$gamma1_S3 <- zeta_S3[1]; mpr_export$gamma2_S3 <- zeta_S3[2]
  mpr_export$kappa1_S3 <- zeta_S3[3]; mpr_export$kappa2_S3 <- zeta_S3[4]
  mpr_export$chi_S3    <- zeta_S3[5]
  mpr_export$P0_S3     <- 100.0
}

write_json(mpr_export, file.path(export_path, "mpr.json"), auto_unbox = TRUE, digits = 8)

# États de calibration
if (!is.null(res_MPR$etats)) {
  write.csv(res_MPR$etats, file.path(export_path, "etats_calibration.csv"), row.names = FALSE)
}
cat("  Done: mpr.json, etats_calibration.csv\n")

# ── 6. Sensibilité MPR ───────────────────────────────────────────────────────
cat("[5/6] Export sensibilité MPR…\n")
res_finaux <- tryCatch(
  readRDS(file.path(base_path, "resultats_finaux_bon_.rds")),
  error = function(e) NULL
)

if (!is.null(res_finaux) && all(c("df_g1","df_g2","df_k1","df_k2","df_chi") %in% names(res_finaux))) {
  df_sens <- rbind(
    cbind(param = "gamma1", res_finaux$df_g1[, c("gamma1_val","prix")] %>%
            rename(param_value = gamma1_val, price = prix)),
    cbind(param = "gamma2", res_finaux$df_g2[, c("gamma2_val","prix")] %>%
            rename(param_value = gamma2_val, price = prix)),
    cbind(param = "kappa1", res_finaux$df_k1[, c("kappa1_val","prix")] %>%
            rename(param_value = kappa1_val, price = prix)),
    cbind(param = "kappa2", res_finaux$df_k2[, c("kappa2_val","prix")] %>%
            rename(param_value = kappa2_val, price = prix)),
    cbind(param = "chi",    res_finaux$df_chi[, c("chi_val","prix")] %>%
            rename(param_value = chi_val, price = prix))
  )
  write.csv(df_sens, file.path(export_path, "sensitivity.csv"), row.names = FALSE)
  cat("  Done: sensitivity.csv\n")
} else {
  cat("  AVERTISSEMENT: résultats_finaux_bon_.rds introuvable ou structure inattendue.\n")
  cat("  Essai avec les colonnes alternatives…\n")
  # Tentative avec noms de colonnes alternatifs du Rmd
  if (!is.null(res_finaux)) {
    tryCatch({
      dfs <- list(
        gamma1 = if ("df_g1" %in% names(res_finaux)) res_finaux$df_g1 else NULL,
        gamma2 = if ("df_g2" %in% names(res_finaux)) res_finaux$df_g2 else NULL,
        kappa1 = if ("df_k1" %in% names(res_finaux)) res_finaux$df_k1 else NULL,
        kappa2 = if ("df_k2" %in% names(res_finaux)) res_finaux$df_k2 else NULL,
        chi    = if ("df_chi" %in% names(res_finaux)) res_finaux$df_chi else NULL
      )
      rows <- list()
      for (nm in names(dfs)) {
        df_nm <- dfs[[nm]]
        if (!is.null(df_nm)) {
          # Trouver colonnes param_value et price
          pv_col <- grep("val|param|value", colnames(df_nm), value=TRUE, ignore.case=TRUE)[1]
          pr_col <- grep("prix|price|P0", colnames(df_nm), value=TRUE, ignore.case=TRUE)[1]
          if (!is.na(pv_col) && !is.na(pr_col)) {
            rows[[nm]] <- data.frame(param=nm, param_value=df_nm[[pv_col]], price=df_nm[[pr_col]])
          }
        }
      }
      if (length(rows) > 0) {
        write.csv(do.call(rbind, rows), file.path(export_path, "sensitivity.csv"), row.names=FALSE)
        cat("  Done: sensitivity.csv (colonnes détectées automatiquement)\n")
      }
    }, error = function(e) cat("  ERREUR sensitivity:", conditionMessage(e), "\n"))
  }
}

# ── Résumé final ─────────────────────────────────────────────────────────────
cat("\n=== Export terminé ===\n")
cat(sprintf("Dossier : %s\n", export_path))
cat("Fichiers générés :\n")
for (f in list.files(export_path)) cat(sprintf("  ✓ %s\n", f))
cat("\nLance maintenant le dashboard :\n")
cat("  cd C:/Users/LGC/Desktop/Memoire/mortality_dashboard\n")
cat("  streamlit run app.py\n")
