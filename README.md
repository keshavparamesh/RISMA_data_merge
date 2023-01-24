# Preperation of RISMA soil moisture observed data

1) This script reads all the downloaded RIMSA 15 minute weather station data (provided all the parameters are in similar format).
2) It combines all the .csv files to one dataframe.
3) It removes all "No Data" & "No Sensor" when the weather stations fail to read soil moisture or if the sensor is damaged
4) The resampling command fills all the missing data with values from the previous rows,
5) Since the resampled data is done hourly, all the 15, 30, 45minute data are removed and only hourly data are retained
6) It removes any duplicate dates and removes negative value
7) It provides average of 3 sesnors each for 5, 20, 50 and 100cm depth soil moisture data
8) Finally it removes hourly data for October - Feburary months from particular range of years
9) The final output is hourly datetime with averages 5, 20, 50 and 100cm soil moisture observed data.







Acknowledging the assistance of Dr. Sriram Subramanian for building the script