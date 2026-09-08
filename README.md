# Background Seismicity Rate Estimation (`BackgroundRateEstimate`)

[![DOI: 10.1093/gji/ggag341](https://img.shields.io/badge/DOI-10.1093%2Fgji%2Fggag341-blue.svg)](https://doi.org/10.1093/gji/ggag341)
[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.15508803.svg)](https://doi.org/10.5281/zenodo.15508803)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides tools to estimate background seismicity rates and benchmarks the results using the **Nearest-Neighbor (NN) distance approach**  , interevent-time **Gamma Distribution Fit** (Hainzl et al., 2006) and  **Reasenberg (1985)** declustering. To evaluate method accuracy against known ground truth, synthetic seismicity catalogs are generated using the **Epidemic-Type Aftershock Sequence (ETAS)** model.

The complete workflow is demonstrated using the **Hawaii ANSS ComCat catalog** ([USGS Earthquake Hazards Program, 2025](https://earthquake.usgs.gov/earthquakes/search/)).

---

## Citation

Read more:

> **Rinty, S. M., & Goebel, T. H. W. (2026).** Characterizing differences in seismicity clustering and background rates between Hawaii and California. *Geophysical Journal International*, 247(1), ggag341. https://doi.org/10.1093/gji/ggag341

### BibTeX

```bibtex
@article{rinty_goebel_2026_gji,
  author    = {Rinty, Sadia Marium and Goebel, Thomas H. W.},
  title     = {Characterizing differences in seismicity clustering and background rates between Hawaii and California},
  journal   = {Geophysical Journal International},
  volume    = {247},
  number    = {1},
  pages     = {ggag341},
  year      = {2026},
  doi       = {10.1093/gji/ggag341},
  url       = {[https://doi.org/10.1093/gji/ggag341](https://doi.org/10.1093/gji/ggag341)}
}
```

To cite the archived software package directly:

```bibtex
@software{rinty_goebel_2025_zenodo,
  author       = {Rinty, Sadia Marium and Goebel, Thomas H. W.},
  title        = {Background Seismicity Rate Estimation},
  month        = may,
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v1.0.1},
  doi          = {10.5281/zenodo.15508803},
  url          = {[https://doi.org/10.5281/zenodo.15508803](https://doi.org/10.5281/zenodo.15508803)}
}
```

---

## Methodological Framework

* **Nearest-Neighbor Clustering:** Based on the space-time-magnitude metric defined by [Zaliapin & Ben-Zion (2013)](https://doi.org/10.1002/jgrb.50179) and adapted from [Goebel et al. (2019)](https://doi.org/10.1016/j.epsl.2019.06.036) ([clustering-analysis repository](https://github.com/tgoebel/clustering-analysis)). The routines have been customized for this dataset.
* **Gamma Distribution Fit:** Quantifies background rate behavior from interevent-time distributions following [Hainzl et al. (2006)](https://doi.org/10.1785/0120050053).
* **Reasenberg Declustering:** Deterministic window-based declustering benchmarked following [Reasenberg (1985)](https://doi.org/10.1029/JB090iB07p05479).
* **Synthetic Benchmark (ETAS):** Synthetic stochastic catalogs with known background rates are generated using the ETAS model by [Mizrahi et al. (2023)](https://doi.org/10.5281/zenodo.7584575) ([lmizrahi/etas](https://github.com/lmizrahi/etas)).

---

## Dependencies & Installation

This project requires **Python 3.7+**.

Install the core Python libraries:

```bash
pip install numpy scipy matplotlib obspy pandas
```

* **Basemap:** Install `basemap` via conda or prebuilt wheels if required for geospatial plotting:
  ```bash
  conda install -c conda-forge basemap
  ```
* **ETAS Package:** Generating synthetic catalogs requires the `etas` package. Follow the setup instructions at [github.com/lmizrahi/etas](https://github.com/lmizrahi/etas).

---

## Repository Structure

```text
BackgroundRateEstimate/
├── code/               # Scripts for fractal analysis, NND computation, and rate estimation
├── ETAS/               # Scripts to simulate synthetic ETAS catalogs
├── data/               # Raw input earthquake catalogs (e.g., ANSS Hawaii)
├── data_processed/     # Rescaled metrics (T, R, eta) and declustered catalogs
├── plots/              # Output figures, distribution fits, and rate comparisons
├── r85/                # Declustered catalogs generated via Reasenberg (1985)
└── README.md
```

---

## Catalog Format

Input catalogs (downloaded via ObsPy or USGS ComCat) are structured as follows:

```text
['YR', 'MO', 'DY', 'HR', 'MN', 'SC', 'N', 'Lat', 'Lon', 'Depth', 'Mag']
```

`EqCat.py` contains utility functions to ingest and format catalogs for Nearest-Neighbor Distance (NND) analysis across various input structures (e.g., relocated catalogs, ANSS ComCat, USGS Hazard Model catalogs).

---

## Step-by-Step Workflow

1. **Catalog Ingestion & Formatting:** Format the raw seismicity catalog using `EqCat.py` to ensure proper space, time, and magnitude column alignment.
2. **Fractal Dimension Analysis:** Run `code/1_fractal_analysis.py` to calculate the spatial fractal dimension ($d_f$) and catalog $b$-value.
3. **Nearest-Neighbor Distance Calculation:** Run `code/2_NND_analysis.py` to compute rescaled time ($T$), rescaled space ($R$), and nearest-neighbor distance ($\eta$).
4. **Background Rate Estimation & Benchmarking:** Run `code/3_estimate_background_rate.py` to estimate background rates and compare results across:
   * Nearest-Neighbor declustering
   * Gamma distribution fit
   * Reasenberg (`r85`) declustering
   * ETAS synthetic catalog ground-truth rates

---

## References

1. **Zaliapin, I., & Ben-Zion, Y. (2013).** Earthquake clusters in southern California I: Identification and stability. *Journal of Geophysical Research: Solid Earth*, 118(6), 2847–2864. https://doi.org/10.1002/jgrb.50179
2. **Goebel, T. H. W., Rosson, Z., Brodsky, E. E., & Walter, J. I. (2019).** Aftershock deficiency of induced earthquake sequences during rapid mitigation efforts in Oklahoma. *Earth and Planetary Science Letters*, 522, 135–143. https://doi.org/10.1016/j.epsl.2019.06.036
3. **Hainzl, S., Scherbaum, F., & Beauval, C. (2006).** Estimating background activity based on interevent-time distribution. *Bulletin of the Seismological Society of America*, 96(1), 313–320. https://doi.org/10.1785/0120050053
4. **Reasenberg, P. (1985).** Second-order moment of central California seismicity, 1969–1982. *Journal of Geophysical Research*, 90(B7), 5479–5495. https://doi.org/10.1029/JB090iB07p05479
5. **Mizrahi, L., Schmid, N., & Han, M. (2023).** lmizrahi/etas: Etas with fit visualization (v3.2). *Zenodo*. https://doi.org/10.5281/zenodo.7584575
6. **U.S. Geological Survey, Earthquake Hazards Program (2025).** Advanced National Seismic System (ANSS) Comprehensive Catalog (ComCat). https://doi.org/10.5066/F7MS3QZH
