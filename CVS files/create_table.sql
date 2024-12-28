CREATE TABLE users (
 id INT AUTO_INCREMENT PRIMARY KEY,
 username VARCHAR(255) NOT NULL UNIQUE,
 password VARCHAR(64) NOT NULL
);



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



DELIMITER // 

CREATE PROCEDURE UpdateTables( 
    IN date DATE, 
    IN country VARCHAR(255), 
    IN new_cases INT 
) 
BEGIN 
    DECLARE old_new_cases INT; 

    -- retrieve the old value of New_cases and store it in old_new_cases 
    SELECT New_cases INTO old_new_cases 
    FROM full_grouped 
    WHERE Date = date 
    AND Country_Region = country; 

    UPDATE full_grouped 
    SET New_cases = new_cases 
    WHERE Date = date 
    AND Country_Region = country; 

    UPDATE full_grouped 
    SET Confirmed = Confirmed - old_new_cases + new_cases,  
        Active = Active - old_new_cases + new_cases 
    WHERE Date >= date 
    AND Country_Region = country; 

    UPDATE day_wise 
    SET New_cases = New_cases - old_new_cases + new_cases 
    WHERE Date = date; 

    UPDATE day_wise 
    SET Confirmed = Confirmed - old_new_cases + new_cases,  
        Active = Active - old_new_cases + new_cases 
    WHERE Date >= date; 

    UPDATE worldometer_data 
    SET TotalCases = TotalCases - old_new_cases + new_cases,  
        ActiveCases = ActiveCases - old_new_cases + new_cases 
    WHERE Country_Region = country; 

    UPDATE country_wise_latest 
    SET Confirmed = Confirmed - old_new_cases + new_cases,  
        Active = Active - old_new_cases + new_cases 
    WHERE Country_Region = country; 

END 
// 

DELIMITER ; 




