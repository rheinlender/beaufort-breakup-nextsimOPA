# Sea ice Breakup in nextSIM-OPA model

This repository contains data, python-scripts and notebooks for analysing and plotting output from the nextSIM-OPA model used in the manuscript "Breaking the Ice: Exploring the Changing Dynamics of Winter Breakup Events in the Beaufort Sea" for JGR: Oceans.  

The Jupyer Notebooks in `notebooks` were developed using the NIRD-Toolkit: a Kubernetes based cloud infrastructure. The `src` directory contains python scripts and functions for analysing the output from the neXtSIM sea-ice model. Relevant grid files are found in `grid_files`. 

## Data

The data is based on the NANUK025-ILBOXE140-S simulation from the neXtSIM-OPA coupled ocean-sea-ice model. The simulation is the same as presented in (Boutin et al., 2022 and Regan et al., 2023). 

Monthly outputs of all quantities are available on Zenodo as NetCDF files at https://doi.org/10.5281/Zenodo.7277523 (Boutin et al., 2022) 

Volume and area fluxes in the Beaufort region were computed by H. Regan and are located in `data_input`.

## Contributors

- Jonathan W. Rheinlænder (jonathan.rheinlaender@nersc.no)
- Heather Regan (heather.regan@nersc.no)
- Guillaume Boutin (guillaume.boutin@nersc.no)

## References 

Boutin, G., Ólason, E., Rampal, P., Regan, H., Lique, C., Talandier, C., Brodeau, L., and Ricker, R.: Arctic sea ice mass balance in a new coupled ice–ocean model using a brittle rheology framework, The Cryosphere, 17, 617–638, https://doi.org/10.5194/tc-17-617-2023, 2023. 

Regan, H., Rampal, P., Ólason, E., Boutin, G., and Korosov, A.: Modelling the evolution of Arctic multiyear sea ice over 2000–2018, The Cryosphere, 17, 1873–1893, https://doi.org/10.5194/tc-17-1873-2023, 2023. 