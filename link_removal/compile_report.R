# Wrapper to render Disruption_Results.Rmd

options(warn = -1)

source('Rutil.R')

library(rmarkdown)

args <- commandArgs(trailingOnly = TRUE)

base_scen <- args[1]
background_flows <- args[2]
disruption_type <- args[3]

render('Disruption_Results.Rmd',
       params = list(
         base_scen = base_scen,
         background_flows = background_flows,
         disrupt_type = disrupt_type)
       )
