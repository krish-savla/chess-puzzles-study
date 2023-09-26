# following tutorial https://www.rensvandeschoot.com/brms-wambs/

library(brms) # for the analysis
library(tidyverse) # needed for data manipulation.
library(RColorBrewer) # needed for some extra colours in one of the graphs
library(ggmcmc)
library(mcmcplots) 

load('brms_results/1/elo ~ wavelength + avg + sd  + (1 + wavelength | pid).RData')

summary(model)

stanplot(model, type="trace")

mdlpost <- as.mcmc(model)

# gelman is very close to 1 for all 1.01 for two, but okay. 
gelman.diag(mdlpost[,1:10])
gelman.plot(mdlpost[,1:10])

# double convergence
#...

# does posterior distribution histogram have enough info?
stanplot(model, type="hist")


# do chains exhibit a strong degree of autocorrelation?

# do posterior distributions make sense?
mcmcplot(model)