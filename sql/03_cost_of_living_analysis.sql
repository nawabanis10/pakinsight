# cost of living
use pakinsight;
DESCRIBE cost_of_living;
SELECT
    item,
    unit,
    islamabad,
    lahore,
    karachi,
    peshawar,
    quetta
FROM cost_of_living
ORDER BY item;

SELECT
    item,
    unit,
    GREATEST(
        islamabad,
        lahore,
        karachi,
        peshawar,
        quetta
    ) AS Highest_Price,
    CASE
        WHEN islamabad = GREATEST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Islamabad'
        WHEN lahore = GREATEST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Lahore'
        WHEN karachi = GREATEST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Karachi'
        WHEN peshawar = GREATEST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Peshawar'
        ELSE 'Quetta'
    END AS Most_Expensive_City
FROM cost_of_living
ORDER BY Highest_Price DESC;


SELECT
    'Islamabad' AS City,
    ROUND(AVG(islamabad), 2) AS Average_Price
FROM cost_of_living

UNION ALL

SELECT
    'Lahore',
    ROUND(AVG(lahore), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Karachi',
    ROUND(AVG(karachi), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Peshawar',
    ROUND(AVG(peshawar), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Quetta',
    ROUND(AVG(quetta), 2)
FROM cost_of_living

ORDER BY Average_Price DESC;


select item,unit,
greatest(islamabad,lahore,karachi,peshawar,quetta)as highest_Price,
least(islamabad,lahore,karachi,peshawar,quetta)as lowest_Price,
round(greatest(islamabad,lahore,karachi,peshawar,quetta)
-
least(islamabad,lahore,karachi,peshawar,quetta),2) as Price_Difference
from cost_of_living
order by Price_Difference;


SELECT
    item,
    unit,
    LEAST(
        islamabad,
        lahore,
        karachi,
        peshawar,
        quetta
    ) AS Lowest_Price,

    CASE
        WHEN islamabad = LEAST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Islamabad'
        WHEN lahore = LEAST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Lahore'
        WHEN karachi = LEAST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Karachi'
        WHEN peshawar = LEAST(islamabad, lahore, karachi, peshawar, quetta)
            THEN 'Peshawar'
        ELSE 'Quetta'
    END AS Cheapest_City

FROM cost_of_living
ORDER BY item;


SELECT
    'Islamabad' AS City,
    ROUND(STDDEV_POP(islamabad), 2) AS Price_Variation
FROM cost_of_living

UNION ALL

SELECT
    'Lahore',
    ROUND(STDDEV_POP(lahore), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Karachi',
    ROUND(STDDEV_POP(karachi), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Peshawar',
    ROUND(STDDEV_POP(peshawar), 2)
FROM cost_of_living

UNION ALL

SELECT
    'Quetta',
    ROUND(STDDEV_POP(quetta), 2)
FROM cost_of_living

ORDER BY Price_Variation DESC;