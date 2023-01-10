# Homicides and Unsolved Cases 2001 - 2021 Chicago 
This repository containes an exploratory data analysis examining the case status of homicides in Chicago by victim characteristics and regional demographics over the last 20 years. I consider the characteristics of homicides, crime trends, how long it takes to clear a specific type of homicide, and what areas (by police district, ward, and neighborhood) of Chicago are most heavily impacted. More data is required to assess the specific causes of these disparities.

## Homicide in Chicago 
The Covid-19 pandemic was met with murder rates almost double of any year over the last two decades—with Black people making up 20-30 times the number of homicide victimizations of every racial group except for White Hispanics. Between 2019 and 2021, more than 1500 Black individuals were murdered in Chicago. Among White Hispanics, nearly 300 people died due to homicide and nearly 100 homicide victims were White. 

## Clearance Rates
The Chicago Police Department relies on the FBI’s formula for calculating clearance rates as the number of homicide cases solved, regardless of the year the incident occurred, divided by the number of homicides committed in a given year. In 2020, CPD cleared 354 homicides and the city saw 774 incidents of homicide resulting in a 45% clearance rate. Almost a fifth of the cases contributing to the clearance rate in 2020 took place prior to 2016.

Cases can also be cleared by [exceptional means](https://ucr.fbi.gov/crime-in-the-u.s/2017/crime-in-the-u.s.-2017/topic-pages/clearances). In the data provided CPD has two categories for exceptional clearance: 'death of offender' and 'bar to prosecution', indicating a suspect was identified but the State Attorney's for whatever reason is unable to charge and prosecute the offender. 

## Data 
The analysis uses homicide clearance data provided by the Chicago Police Department in response to a Freedom of Information Act request made by LiveFree Illinois (an organization advocating for police accountability in Chicago) and it includes homicides that were cleared between 2019 and 2021. Please [contact me](mailto:prozhkova7@gmail.com) if you are interested in using this data. This project also relies on victimization data available on the [Chicago Data Portal - Violence Reduction](https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Victims-of-Homicides-and-Non-Fa/gumc-mgzr) and [Chicago Data Portal - Crime 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2). For cases that were cleared between 2001 and 2018, I use data gathered by [The Trace](https://www.thetrace.org/violent-crime-data/) for their reporting on unsolved murders in 2019.

Throughout the the project, I specify when I'm referring to formal 'clearances rates' versus the number of homicides committed between 2001 and 2021 that have been cleared. Cases counting towards the formal clearances rates for these years may have occurred prior to 2001 and will therefore not be featured. 

## Framework
Academic literature points to two primary theories around racial disparities in homicide clearance rates. One theory suggests that law enforcement makes less of an effort with cases involving non-white victims in disadvantaged neighborhoods and the second theory suggests that law enforcement value all victims equally but factors such as the incident characteristics and detective workload lead to unequal outcomes in a homicide investigation. Proving the validity of either theory is irrelevant to the scope of this work, but the two theories together help provide a framework by which to assess what (if anything) in the existing law enforcement system is working.

## Contents of EDA
- Mapping of homicide counts and clearance rates in Chicago neighborhoods 2019 - 2021
- Demographics of police districts by race
- Number of cases cleared between 2001 - 2021
- Homicide trends over time 
- Domestic violence related homicides 
- Case clearance by race and sex
- Characteristics of an incident 
- Average time to clearance for homicides (in progress)
- Average time to clearance for non fatal shootings (in progress)
- Static plots 
- Interative shiny plots 

## Big picture questions
- Focusing on increasing clearance rates runs the obvious danger of locking up innocent people but if there were a way to ensure that every perpetrator was correctly identified and held accountable for their crimes, what impact would that have on community safety? What effect would that have on overall wellbeing? 
- Is there data on cities with homicide rates comparable to those of Chicago that have significantly improved in response to calls for police reform?
- What would murder accountability look like in the absence of a carceral strategy? 

As a human being, I don't believe in the efficacy of incarceration as a remedy for crime and as a researcher, there is no evidence that America's carceral strategy is working. Countless empirical studies point out that increased incarceration has had close to no effect on the decrease in violent crime since 2000 ([this report](https://www.brennancenter.org/our-work/research-reports/what-caused-crime-decline) highlights several studies). 
