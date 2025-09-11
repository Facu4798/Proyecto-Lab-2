# Plan de experimentación

| Modelo   | Parámetros a probar                        |
|:---------|:-------------------------------------------|
| ARCH     | Lags (p): 1                                |
| ARCH     | Lags (p): 5                                |
| ARCH     | Lags (p): 10                               |
| GARCH    | (p,q): (1,1)                               |
| GARCH    | (p,q): (1,2)                               |
| GARCH    | (p,q): (2,1)                               |
| GARCH    | (p,q): (2,2)                               |
| EGARCH   | (p,q): (1,1) Distribución Normal           |
| EGARCH   | (p,q): (1,1) Distribución t-Student        |
| EGARCH   | (p,q): (2,1) Distribución Normal           |
| EGARCH   | (p,q): (2,1) Distribución t-Student        |
| TGARCH   | (p,q): (1,1) Threshold: 0                  |
| TGARCH   | (p,q): (1,1) Threshold: -0.25*sigma_resid  |
| TGARCH   | (p,q): (1,1) Threshold: -0.5*sigma_resid   |
| TGARCH   | (p,q): (1,1) Threshold: -1.0*sigma_resid   |
| TGARCH   | (p,q): (1,1) Threshold: -2.0*sigma_resid   |
| TGARCH   | (p,q): (1,1) Threshold: percentile 25      |
| TGARCH   | (p,q): (1,1) Threshold: percentile 10      |
| TGARCH   | (p,q): (1,1) Threshold: percentile 5       |
| TGARCH   | (p,q): (1,1) Threshold: percentile 1       |
| TGARCH   | (p,q): (1,1) Threshold: percentile 0.1     |
| TGARCH   | (p,q): (2,1) Threshold: 0                  |
| TGARCH   | (p,q): (2,1) Threshold: -0.25*sigma_resid  |
| TGARCH   | (p,q): (2,1) Threshold: -0.5*sigma_resid   |
| TGARCH   | (p,q): (2,1) Threshold: -1.0*sigma_resid   |
| TGARCH   | (p,q): (2,1) Threshold: -2.0*sigma_resid   |
| TGARCH   | (p,q): (2,1) Threshold: percentile 25      |
| TGARCH   | (p,q): (2,1) Threshold: percentile 10      |
| TGARCH   | (p,q): (2,1) Threshold: percentile 5       |
| TGARCH   | (p,q): (2,1) Threshold: percentile 1       |
| TGARCH   | (p,q): (2,1) Threshold: percentile 0.1     |
| REGARMA  | AR lags: 1, MA lags: 1, GARCH order: (1,1) |
| REGARMA  | AR lags: 1, MA lags: 1, GARCH order: (2,1) |
| REGARMA  | AR lags: 1, MA lags: 5, GARCH order: (1,1) |
| REGARMA  | AR lags: 1, MA lags: 5, GARCH order: (2,1) |
| REGARMA  | AR lags: 5, MA lags: 1, GARCH order: (1,1) |
| REGARMA  | AR lags: 5, MA lags: 1, GARCH order: (2,1) |
| REGARMA  | AR lags: 5, MA lags: 5, GARCH order: (1,1) |
| REGARMA  | AR lags: 5, MA lags: 5, GARCH order: (2,1) |
