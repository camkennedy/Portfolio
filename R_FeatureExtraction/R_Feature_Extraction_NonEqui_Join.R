#This example generates a table of cities with randomly generated 
#sales figures by day (dtData), and then queries that table given 
#parameters in another table (dtQIP). It features a non-equi join,
#allowing summary data to be extracted efficiently from multiple,
#simultaneous conditions. This technique can then be used either 
#to generate quick summaries of data, or in feature extraction
#as part of a larger machine learning exercise.

#This example can be extrapolated to numerous other cases.

#0. Load libraries and initialize
library(data.table)
set.seed(77)  #To obtain consistent results
gc()

#1. Generate Long Grid of City and Day
system.time(
  dtData <- data.table(expand.grid(City = c("Denver", "Seattle", "Chicago", "New York"),
                                   Day = seq(1, 1e6, 1) 
                                   #1e6 = 1M days.  Times 4 cities = 4M rows
                                   )
                       )
  )
#Optional: To test impressive data.table speed, increase 1e6 to 1e7 --> 40M rows!

#2. Generate random Sales figures between 0 and 100
dtData[, Sales := floor(runif(.N)*101)] 
  #Note the .N produces a vector of random numbers the length of the data table.  
  #Runif(1) would just produce the same number for the entire column.

#3. Generate Query Input Parameters table 
dtQIP <- data.table(City = c("Denver", "Seattle", "Chicago", "New York", "Denver"),
                    SalesAtLeast = c(20L, 30L, 40L, 50L, 45L),
                    FromDay = c(100L, 50L, 50L, 100L, 100L),
                    UntilDay = c(2000L, 2000L, 1000L, 3500L, 2000L)
)

#4a. Join tables to aggregate results based on dtQIP inputs.
system.time(
  dtResults <- dtData[dtQIP,  #Left join (backwards in data.table). QIP=Query Imput Parameters
                      #Non-equi join parameters
                      on=.(City=City, Sales>=SalesAtLeast, Day>=FromDay, Day<=UntilDay),
                      #Elements to include.  x=Left side; i=Right side
                      .(i.City, i.SalesAtLeast, i.FromDay, i.UntilDay, x.Day, x.Sales)][
                        #Aggregation elements
                        , .(count=.N, sum=sum(x.Sales)),
                        #Group by elements. Good practice to include all parameters to avoid accidental duplication, and to preserve original dtQIP table.
                        by=.(i.City, i.SalesAtLeast, i.FromDay, i.UntilDay)]
)
#The first data table makes a long list of the individual rows that meet the criteria in dtQIP.
#The second one (chained using ][ ) performs the aggregation and grouping.
View(dtResults)


#4b. Similar code to 4a above, but split out to produce an interim 
#table to better see what's happening.
system.time(
  dtInterim <- dtData[dtQIP,
                      on=.(City=City, Sales>=SalesAtLeast, Day>=FromDay, Day<=UntilDay),
                      .(i.City, i.SalesAtLeast, i.FromDay, i.UntilDay, x.Day, x.Sales)]
)

#Generate results by summarizing table.
dtResults2 <- dtInterim[, .(count=.N, sum=sum(x.Sales)),
                        by=.(i.City, i.SalesAtLeast, i.FromDay, i.UntilDay)]
View(dtInterim)
View(dtResults2)
