# FTOT-Resilience-Link_Removal

FTOT Resilience Tool: Link Removal tool for assessing network resilience.

See the [FTOT homepage](https://volpeusdot.github.io/FTOT-Public/) for general information about the Freight and Fuel Transportation Optimization Tool (FTOT).

This tool runs disruptions of an optimal solution, using a network property known as betweenness centrality, or by using the volume of vehicles on roadway links. The tool assesses how resilient an optimal solution is to the removal of key links in the network.

#### Requirements

- `conda`
- FTOT code
- FTOT documentation and scenarios
- 10-25 GB free hard disk space

## Install `conda`

This tool relies on the  package management software `conda` to add all dependencies for this tool, separate from the standard FTOT requirements.

You need either [miniconda](https://docs.conda.io/en/latest/miniconda.html) (1.2 mb) or the full [Anaconda](https://www.anaconda.com/products/distribution) (500+ mb) installation to activate a conda environment. The full Anaconda installation is recommended for most users.

## Install FTOT code

[Download and install FTOT](https://github.com/VolpeUSDOT/FTOT-Public/wiki/FTOT-Installation-Guide) if you haven't already done so, and install the documentation and scenarios.

Run `simple_setup.bat` to ensure you have a correct Python environment set up for FTOT.

Run QS1 and QS2 to verify that the installation is complete.

## Modify FTOT

Two files in the FTOT code need to be modified for this use case. They are as follows:

- `ftot_networkx.py`
	+ Modified to keep temporary shapefiles. This adds size to the output of each scenario, but allows us to make modifications to the shapefiles
- `ftot_routing.py`
	+ Modified to not add back in interstates to the road network. Without this step, an analysis of the road network would always include the national interstate system.
	+ Also modified to use only a 50 mile buffer around the selected area. This makes the scenario analysis more specific to the local network.

You can either copy the versions of these two files into your installed FTOT, or use the complete version of FTOT in this repository, which has modified these files. To do the latter, place the contents of this repository in `C:\FTOT\program`.

## Using this code

This code is written for Python 3.x, using Jupyter Notebooks to interact with the outputs of FTOT runs, calculate evenness as a proxy of resiliency, and carry out sequential link removal and recalculation of network performance.

The Python dependences are detailed in `environment.yml`. This assumes you have an installation of Python 3.x and conda. These steps follow [this reference](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file). You only need to create the environment once.

From your Anaconda Prompt, navigate to the location where you cloned this repository, and then navigate to the `\link_removal` subfolder and run the following:

```
conda env create -f environment.yml
```

You should see `FTOTnetworkEnv` show up as an available environment, when checking your environments with:

```
conda info --envs
```

You can then launch Jupyter Notebook by the following steps:

```
conda activate FTOTnetworkEnv
jupyter notebook
```

You only need to create the environment once; thereafter, you can simply `conda activate FTOTnetworkEnv` and `jupyter notebook`.

If the Jupyter Notebook instance launches with a warning about the kernel, you may need to manually select `FTOTnetworkEnv` as the kernel to use.


## Run Reference Scenario 1

Run Reference Scenario 1 now, using the modified FTOT code.
Browse to `C:\FTOT\scenarios\reference_scenarios\rs1_multi_commodity_supply_chain` and double-click `run_v6_1.bat`.

## Conduct link removal disruptions

From the Jupyter Notebook window, browse to `Conduct_Link_Removal.ipynb` to begin this module.
