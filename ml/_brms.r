#!/usr/bin/env Rscript

# TODO: for each participant; drop the first 2 and last 2 puzzles. 
# TODO: interaction effect between probe, wavelength, and average / probe, wavelength, sd

library(brms)

load("DF.RData")

# formulae run
# 

formulae <- c("elo ~ wavelength + avg + sd + probe + (1 | pid)", 
			  "elo ~ wavelength + avg + sd + (1 | pid)", 
			  "elo ~ wavelength*avg + wavelength*sd + (1 | pid)", 
			  "elo ~ wavelength:avg:sd:probe + (1 | pid)",
			  "elo ~ wavelength:avg:sd:probe + (1 + wavelength:avg:sd:probe | pid)",
			  "elo ~ wavelength + avg + sd  + (1 + wavelength | pid)",
			  "elo ~ wavelength + avg + sd  + (1 + wavelength + avg | pid)",
			  "elo ~ wavelength + avg + sd  + (1 + wavelength + avg + sd | pid)",
			  "elo ~ 1 + (1 | pid)")

args       <- commandArgs(trailingOnly=TRUE)
formulaNum <- as.numeric(args[1])
formulaStr <- formulae[formulaNum]
formula    <- as.formula(formulaStr)
saveFile   <- paste(formulaStr, "RData", sep=".")

model <- brms::brm(formula, 
		   		   data=df, threads=threading(4), cores=4, 
		           control = list(adapt_delta = .99), 
		           seed = 123) 

save(model, file = saveFile)

  

