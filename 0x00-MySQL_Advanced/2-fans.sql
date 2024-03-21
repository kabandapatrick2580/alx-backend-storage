-- SQL script to rank bands by country of origin based on the number of unique fans

-- Select the country of origin and calculate the total number of fans for each country
SELECT origin, SUM(fans) AS num_fans
FROM metal_bands
GROUP BY origin -- Group the bands by their country of origin
ORDER BY num_fans DESC; -- Order the results by the total number of fans in descending order
