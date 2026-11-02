# weather data

use pakinsight;

describe weather_data;

select city,
round(avg(temp_max),2) as Avg_max_temp,
round(avg(temp_min),2)as Avg_min_temp
from weather_data
group by city
order by Avg_max_temp desc;


select city,
round(sum(precipitation),2) as Total_annual_rainfall,
round(avg(precipitation),2) as Avg_daily_rainfall
from weather_data
group by city
order by Total_annual_rainfall desc;


SELECT
    City,
    Month_Name,
    Avg_Max_Temperature
FROM (
    SELECT
        city AS City,
        MONTHNAME(date) AS Month_Name,
        MONTH(date) AS Month_Number,
        ROUND(AVG(temp_max), 2) AS Avg_Max_Temperature,
        ROW_NUMBER() OVER (
            PARTITION BY city
            ORDER BY AVG(temp_max) DESC
        ) AS Month_Rank
    FROM weather_data
    GROUP BY city, MONTH(date), MONTHNAME(date)
) AS Monthly_Temperatures
WHERE Month_Rank = 1
ORDER BY Avg_Max_Temperature DESC;


SELECT
    City,
    Month_Name,
    Avg_Min_Temperature
FROM (
    SELECT
        city AS City,
        MONTHNAME(date) AS Month_Name,
        ROUND(AVG(temp_min), 2) AS Avg_Min_Temperature,
        ROW_NUMBER() OVER (
            PARTITION BY city
            ORDER BY AVG(temp_min) ASC
        ) AS Month_Rank
    FROM weather_data
    GROUP BY city, MONTH(date), MONTHNAME(date)
) AS Monthly_Temperatures
WHERE Month_Rank = 1
ORDER BY Avg_Min_Temperature ASC;