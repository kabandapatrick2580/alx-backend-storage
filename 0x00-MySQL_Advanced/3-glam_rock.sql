-- Create a temporary table to store band names and their lifespan
CREATE TEMPORARY TABLE IF NOT EXISTS temp_band_lifespan AS
    SELECT
        band_name,
        -- Calculate the lifespan in years until 2022
        ROUND(DATEDIFF(IFNULL(split, '2022-01-01'), CONCAT(formed, '-01-01')) / 365, 2) AS lifespan
    FROM
        metal_bands
    WHERE
        style LIKE '%Glam rock%';

-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, lifespan
FROM temp_band_lifespan
ORDER BY lifespan DESC;
