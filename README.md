# FTOT-Resilience-Link_Removal

FTOT Resilience Tool: Link Rank and Removal tool for assessing network resilience.

See the [FTOT homepage](https://volpeusdot.github.io/FTOT-Public) for general information about the Freight and Fuel Transportation Optimization Tool (FTOT).

This tool runs disruptions of an optimal solution, removing network links sequentially based on one of two metrics: (1) a network property known as betweenness centrality, or (2) the volume of vehicles on roadway links. The tool assesses how resilient an optimal solution is to the removal of key links in the network.

This tool is compatible and has been tested with FTOT version [2024.1](https://github.com/VolpeUSDOT/FTOT-Public/releases/tag/2024.1) and will not work with previous versions of FTOT. This tool is compatible only with FTOT scenarios using **only** the road network and for which Network Density Reduction (NDR) is off. To confirm NDR is off, check the the NDR_On element in the scenario XML file is set to False.

#### Requirements

- `conda`
- FTOT code
- FTOT documentation and scenarios
- 10-25 GB free hard disk space

## Install `conda`

This tool relies on the package management software `conda` to add all dependencies for this tool, separate from the standard FTOT requirements.

You need either [miniconda](https://docs.conda.io/en/latest/miniconda.html) (1.2 mb) or the full [Anaconda](https://www.anaconda.com/products/distribution) (500+ mb) installation to activate a conda environment. The full Anaconda installation is recommended for most users.

## Install FTOT code

[Download and install FTOT](https://volpeusdot.github.io/FTOT-Public/#getting-started) if you haven't already done so, and [download the documentation and scenarios](https://volpeusdot.github.io/FTOT-Public/data_download.html).

Run `simple_setup.bat` to ensure you have a working Python environment set up for FTOT.

Run Quick Start 1 and Quick Start 2 to verify that the installation is complete.

## Modify FTOT

One file in the FTOT code needs to be modified for this resilience tool:

- `ftot_routing.py`
	+ Modified to not add back in all interstates to the road network. Without this edit, an FTOT analysis of the road network always includes the national interstate system.
	+ Modified to use only a 50 mile buffer around the selected area. This makes the scenario analysis more specific to the local network of the FTOT analysis.

You can either copy the version of this file from this repository into your installed FTOT directory (e.g., `C:\FTOT\program`), or use the complete version of FTOT included in this repository, which has already modified the file. To do the latter, place all of the contents of the `\program` subfolder in this repository into `C:\FTOT\program`.

## Using this code

This code is written for Python 3.9, using Jupyter Notebooks to interact with the outputs of FTOT runs, calculate network resiliency metrics, and carry out sequential link removal and recalculation of network performance.

The Python dependencies for this resilience tool are detailed in `environment.yml` in the `\link_removal` subfolder. The following steps use [this reference](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) and assume you have an installation of Python 3.9 and conda.

From your Anaconda Prompt, navigate to the location where you cloned this repository, and then navigate to the `\link_removal` subfolder and run the following:

```
conda env create -f environment.yml
```

You should see `FTOTnetworkEnv` show up as an available environment when checking your environments with:

```
conda info --envs
```

You can then launch Jupyter Notebook by the following steps:

```
conda activate FTOTnetworkEnv
jupyter notebook
```

You only need to create the environment once; thereafter, you can simply run `conda activate FTOTnetworkEnv` and `jupyter notebook`.

If the Jupyter Notebook instance launches with a warning about the kernel, you may need to manually select `FTOTnetworkEnv` as the kernel to use. If the `FTOTnetworkEnv` kernel fails to load, follow [these steps](https://stackoverflow.com/questions/54876404/unable-to-import-sqlite3-using-anaconda-python) to ensure all supporting files are present.

## Run Reference Scenario 7

Run Reference Scenario 7 using the modified FTOT code. Browse to `C:\FTOT\scenarios\reference_scenarios\rs7_capacity` and double-click `run_v7.bat`.

## Conduct link rank and removal disruptions

From the Jupyter Notebook window, browse to `Conduct_Link_Removal.ipynb` to begin this module.
