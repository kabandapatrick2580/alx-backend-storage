-- Create a temporary table to store aggregated fan counts per origin
CREATE TEMPORARY TABLE IF NOT EXISTS temp_origin_fans AS
    SELECT origin, SUM(fans) AS nb_fans
    FROM metal_bands
    GROUP BY origin;

-- Rank country origins of bands by the total number of (non-unique) fans
SELECT origin, nb_fans
FROM temp_origin_fans
ORDER BY nb_fans DESC;
