# Wrapper to render Disruption_Results.Rmd

options(warn = -1)

source('Rutil.R')

library(rmarkdown)

args <- commandArgs(trailingOnly = TRUE)

base_scen <- args[1]

render('Disruption_Results.Rmd',
       params = list(
         base_scen = base_scen)
       )
