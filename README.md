# FTOT-Resilience-Link_Removal

FTOT Resilience Tool: Link Removal tool for assessing network resilience.

See the [FTOT homepage](https://volpeusdot.github.io/FTOT-Public) for general information about the Freight and Fuel Transportation Optimization Tool (FTOT).

This tool runs disruptions of an optimal solution, using a network property known as betweenness centrality, or by using the volume of vehicles on roadway links. The tool assesses how resilient an optimal solution is to the removal of key links in the network.

This tool is compatible and has been tested with FTOT version 2022.3.

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

Two files in the FTOT code need to be modified for this resilience tool. They are as follows:

- `ftot_networkx.py`
	+ Modified to keep temporary shapefiles. This adds size to the output of each scenario, but allows us to make modifications to the shapefiles.
- `ftot_routing.py`
	+ Modified to not add back in interstates to the road network. Without this step, an analysis of the road network would always include the national interstate system.
	+ Modified to use only a 50 mile buffer around the selected area. This makes the scenario analysis more specific to the local network.

You can either copy the versions of these two files from this repository into your installed FTOT directory, or use the complete version of FTOT included in this repository, which has already modified these files. To do the latter, place the contents of this repository in `C:\FTOT\program`.

## Using this code

This code is written for Python 3.x, using Jupyter Notebooks to interact with the outputs of FTOT runs, calculate evenness as a proxy of resiliency, and carry out sequential link removal and recalculation of network performance.

The Python dependencies for this resilience tool are detailed in `environment.yml` in the `\link_removal` subfolder. The following steps use [this reference](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) and assume you have an installation of Python 3.x and conda. You only need to create the environment once.

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

## Run Reference Scenario 1

Run Reference Scenario 1 using the modified FTOT code. Browse to `C:\FTOT\scenarios\reference_scenarios\rs1_multi_commodity_supply_chain` and double-click `run_v7.bat`.

## Conduct link removal disruptions

From the Jupyter Notebook window, browse to `Conduct_Link_Removal.ipynb` to begin this module.
