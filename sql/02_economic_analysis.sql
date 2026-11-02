use pakinsight;
SELECT
    City,
    SUM(Establishments) AS Total_Establishments,
    SUM(Workforce) AS Total_Workforce
FROM economic_categories
GROUP BY City
ORDER BY Total_Establishments DESC;

select City,sum(Establishments) as Manufacturing_Establishments,
sum(WorkForce) as Manufacturing_Workforce from economic_categories
where Description = "Manufacturing"
group by City
order by Manufacturing_Workforce desc ;

select City,sum(Workforce) as Total_workforce
from economic_categories group by City
having Total_workforce >= 500000
order by Total_workforce desc;

SELECT
    es.district,
    es.establishments,
    es.workforce,
    ec.Manufacturing_Workforce
FROM economic_summary AS es
JOIN (
    SELECT
        city,
        SUM(workforce) AS Manufacturing_Workforce
    FROM economic_categories
    WHERE Description = 'Manufacturing'
    GROUP BY city
) AS ec
ON es.district = ec.city
ORDER BY es.workforce DESC;

SELECT DISTINCT district
FROM economic_summary;

SELECT DISTINCT city
FROM economic_categories;

SELECT
    CASE
        WHEN district IN ('Karachi East', 'Karachi West',
                          'Karachi South', 'Karachi Central')
        THEN 'Karachi'
        ELSE district
    END AS city,
    SUM(establishments) AS total_establishments,
    SUM(workforce) AS total_workforce
FROM economic_summary
GROUP BY city;

use pakinsight;

SELECT
    CASE
        WHEN district LIKE 'Karachi%' THEN 'Karachi'
        ELSE district
    END AS City,
    SUM(workforce) AS Total_Workforce,
    CASE
        WHEN SUM(workforce) >= 1000000 THEN 'High Workforce'
        WHEN SUM(workforce) >= 500000 THEN 'Medium Workforce'
        ELSE 'Low Workforce'
    END AS Workforce_Category
FROM economic_summary
GROUP BY City
ORDER BY Total_Workforce DESC;

SELECT
    m.city,
    m.Manufacturing_Workforce,
    w.Avg_Max_Temperature
FROM
(
    SELECT
        city,
        SUM(workforce) AS Manufacturing_Workforce
    FROM economic_categories
    WHERE Description = 'Manufacturing'
    GROUP BY city
) AS m
JOIN
(
    SELECT
        city,
        AVG(temp_max) AS Avg_Max_Temperature
    FROM weather_data
    GROUP BY city
) AS w
ON m.city = w.city
ORDER BY m.Manufacturing_Workforce DESC;


select Description,sum(Establishments) as Total_establishments,
sum(Workforce) as Total_workforce
from economic_categories
group by Description
order by Total_establishments desc limit 5;


SELECT
    City,
    Description AS Top_Sector,
    Total_Workforce
FROM (
    SELECT
        City,
        Description,
        SUM(Workforce) AS Total_Workforce,
        ROW_NUMBER() OVER (
            PARTITION BY City
            ORDER BY SUM(Workforce) DESC
        ) AS Sector_Rank
    FROM economic_categories
    GROUP BY City, Description
) AS Ranked_Sectors
WHERE Sector_Rank = 1
ORDER BY Total_Workforce DESC;


SELECT
    City,
    Description AS Sector,
    SUM(Workforce) AS Sector_Workforce,
    ROUND(
        SUM(Workforce) * 100.0 /
        SUM(SUM(Workforce)) OVER (PARTITION BY City),
        2
    ) AS Workforce_Percentage
FROM economic_categories
GROUP BY City, Description
ORDER BY City, Workforce_Percentage DESC;


SELECT
    CASE
        WHEN district LIKE 'Karachi%' THEN 'Karachi'
        ELSE district
    END AS City,
    SUM(establishments) AS Total_Establishments,
    SUM(workforce) AS Total_Workforce,
    ROUND(
        SUM(workforce) / NULLIF(SUM(establishments), 0),
        2
    ) AS Avg_Workers_Per_Establishment
FROM economic_summary
GROUP BY City
ORDER BY Avg_Workers_Per_Establishment DESC;
