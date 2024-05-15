# Wrapper to render Disruption_Results.Rmd

options(warn = -1)

source('Rutil.R')

library(rmarkdown)

args <- commandArgs(trailingOnly = TRUE)

base_scen <- args[1]
disrupt_type <- args[2]

render('Disruption_Results.Rmd',
       params = list(
         base_scen = base_scen,
         disrupt_type = disrupt_type)
       )
