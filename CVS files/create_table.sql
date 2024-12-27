CREATE TABLE country_wise_latest(
    Country_Region VARCHAR(30),
    Confirmed INT DEFAULT 0,
    Deaths INT DEFAULT 0,
    Recovered INT DEFAULT 0,
    Active INT DEFAULT 0,
    PRIMARY KEY CLUSTERED (Country_Region)
);

LOAD DATA LOCAL INFILE './country_wise_latest.csv'
INTO TABLE country_wise_latest
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Country_Region, Confirmed, Deaths, Recovered, Active);



CREATE TABLE covid_19_clean_complete( 
    Province_State VARCHAR(30), 
    Country_Region VARCHAR(30), 
    Date DATE, 
    Confirmed INT DEFAULT 0, 
    Deaths INT DEFAULT 0, 
    Recovered INT DEFAULT 0, 
    Active INT DEFAULT 0, 
    PRIMARY KEY CLUSTERED (Province_State, Country_Region, Date) 
);

LOAD DATA LOCAL INFILE './covid_19_clean_complete.csv' 
INTO TABLE covid_19_clean_complete 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
ENCLOSED BY '"' 
IGNORE 1 LINES 
(Province_State, Country_Region, Date, Confirmed, Deaths, Recovered, Active);




CREATE TABLE day_wise(
    Date DATE,
    Confirmed INT DEFAULT 0,
    Deaths INT DEFAULT 0,
    Recovered INT DEFAULT 0,
    Active INT DEFAULT 0,
    New_cases INT DEFAULT 0,
    New_deaths INT DEFAULT 0,
    New_recovered INT DEFAULT 0,
    No_of_countries INT DEFAULT 0,
    PRIMARY KEY CLUSTERED (Date)
);

LOAD DATA LOCAL INFILE './day_wise.csv'
INTO TABLE day_wise
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Date, Confirmed, Deaths, Recovered, Active, New_cases, New_deaths, New_recovered, No_of_countries);




CREATE TABLE full_grouped(
    Date DATE,
    Country_Region VARCHAR(30),
    Confirmed INT DEFAULT 0,
    Deaths INT DEFAULT 0,
    Recovered INT DEFAULT 0,
    Active INT DEFAULT 0,
    New_cases INT DEFAULT 0,
    New_deaths INT DEFAULT 0,
    New_recovered INT DEFAULT 0,
    PRIMARY KEY CLUSTERED (Date, Country_Region)
);

LOAD DATA LOCAL INFILE './full_grouped.csv'
INTO TABLE full_grouped
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Date, Country_Region, Confirmed, Deaths, Recovered, Active, New_cases, New_deaths, New_recovered);



CREATE TABLE worldometer_data(
    Country_Region VARCHAR(30),
    Continent VARCHAR(30),
    Population INT DEFAULT 0,
    TotalCases INT DEFAULT 0,
    TotalDeaths INT DEFAULT 0,
    TotalRecovered INT DEFAULT 0,
    ActiveCases INT DEFAULT 0,
    Serious_Critical INT DEFAULT 0,
    TotalTests INT DEFAULT 0,
    PRIMARY KEY CLUSTERED (Country_Region)
);

LOAD DATA LOCAL INFILE './worldometer_data.csv'
INTO TABLE worldometer_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Country_Region, Continent, Population, TotalCases, TotalDeaths, TotalRecovered, ActiveCases, Serious_Critical, TotalTests);



