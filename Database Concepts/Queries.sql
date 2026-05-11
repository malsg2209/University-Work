-- Q1 --
SELECT
    '2021-03-01' AS Date_1,
    loc.location AS Country_Name,
    IFNULL(MAX(CASE WHEN g.date = '2021-03-01' THEN g.total_vaccinations END), 0) AS VOD1,
    '2022-03-01' AS Date_2,
    IFNULL(MAX(CASE WHEN g.date = '2022-03-01' THEN g.total_vaccinations END), 0) AS VOD2,
    '2022-05-01' AS Date_3,
    IFNULL(MAX(CASE WHEN g.date = '2022-05-01' THEN g.total_vaccinations END), 0) AS VOD3,

    -- Calculate the Percentage Change of Totals with 0 for missing values
    IFNULL(
        CASE 
            WHEN MAX(CASE WHEN g.date = '2021-03-01' THEN g.total_vaccinations END) > 0 
                 AND MAX(CASE WHEN g.date = '2022-03-01' THEN g.total_vaccinations END) > 0
            THEN 
                (
                    (
                        (MAX(CASE WHEN g.date = '2022-03-01' THEN g.total_vaccinations END) - 
                         MAX(CASE WHEN g.date = '2021-03-01' THEN g.total_vaccinations END)) / 
                         NULLIF(MAX(CASE WHEN g.date = '2021-03-01' THEN g.total_vaccinations END), 0)
                    ) - 
                    (
                        (MAX(CASE WHEN g.date = '2022-05-01' THEN g.total_vaccinations END) - 
                         MAX(CASE WHEN g.date = '2022-03-01' THEN g.total_vaccinations END)) / 
                         NULLIF(MAX(CASE WHEN g.date = '2022-03-01' THEN g.total_vaccinations END), 0)
                    )
                ) * 100
            ELSE 0
        END,
    0) AS Percentage_Change_of_Totals
FROM
    A_Locations_Summary AS loc
LEFT JOIN 
    G_Vaccination_Population_Total_Data AS g 
    ON loc.loc_id = g.loc_id 
    AND g.date IN ('2021-03-01', '2022-03-01', '2022-05-01')
WHERE 
    loc.location NOT IN (
        'Africa', 'Asia', 'Europe', 'European Union', 'Faeroe Islands', 'Falkland Islands', 
        'Gibraltar', 'Greenland', 'Hong Kong', 'Macao', 'New Caledonia', 'Northern Cyprus', 
        'Oceania', 'Palestine', 'Pitcairn', 'Scotland', 'Sint Maarten (Dutch part)', 'Tokelau', 
        'Turks and Caicos Islands', 'Wales', 'Wallis and Futuna', 'World', 'North America', 
        'South America', 'Aruba', 'Bermuda', 'Bonaire, Sint Eustatius, and Saba', 
        'British Virgin Islands', 'Cayman Islands', 'Cook Islands', 'Curacao', 'England', 
        'French Polynesia', 'Guernsey', 'Isle of Man', 'Jersey', 'Montserrat', 'Niue', 
        'Northern Ireland', 'Pitcairn Islands', 'Saint Helena', 'Taiwan', 'Timor'
    )
GROUP BY
    loc.location
ORDER BY 
    Percentage_Change_of_Totals DESC;



-- Q2 --
SELECT 
    loc.location AS "Country Name",
    strftime('%m', a.date) AS "Month",
    strftime('%Y', a.date) AS "Year",
    
    -- Calculate the Growth Rate as a percentage and ensure it's not NULL, rounded to 2 decimal places
    ROUND(IFNULL(((a.monthly_total - IFNULL(b.monthly_total, 0)) * 100.0 / IFNULL(b.monthly_total, 1)), 0), 2) AS "Growth rate of vaccine (GR)",

    -- Calculate the Difference of Growth Rate to Global Average, rounded to 2 decimal places
    ROUND(IFNULL(((a.monthly_total - IFNULL(b.monthly_total, 0)) * 100.0 / IFNULL(b.monthly_total, 1)) -
    (SELECT AVG((c.monthly_total - IFNULL(d.monthly_total, 0)) * 100.0 / IFNULL(d.monthly_total, 1))
     FROM (
         SELECT loc_id, 
                strftime('%Y-%m', date) AS month_year,
                SUM(daily_vaccinations) AS monthly_total
         FROM F_Vaccination_Daily_Data
         GROUP BY loc_id, strftime('%Y-%m', date)
     ) AS c
     LEFT JOIN (
         SELECT loc_id, 
                strftime('%Y-%m', date) AS month_year,
                SUM(daily_vaccinations) AS monthly_total
         FROM F_Vaccination_Daily_Data
         GROUP BY loc_id, strftime('%Y-%m', date)
     ) AS d 
     ON c.loc_id = d.loc_id AND c.month_year = strftime('%Y-%m', DATE(d.month_year || '-01', '+1 month'))
     WHERE c.month_year = strftime('%Y-%m', a.date)
    ), 0), 2) AS "Difference of growth rate to global average"

FROM (
    SELECT loc_id, 
           strftime('%Y-%m', date) AS month_year,
           SUM(daily_vaccinations) AS monthly_total,
           date
    FROM F_Vaccination_Daily_Data
    GROUP BY loc_id, strftime('%Y-%m', date)
) AS a
LEFT JOIN (
    SELECT loc_id, 
           strftime('%Y-%m', date) AS month_year,
           SUM(daily_vaccinations) AS monthly_total
    FROM F_Vaccination_Daily_Data
    GROUP BY loc_id, strftime('%Y-%m', date)
) AS b 
ON a.loc_id = b.loc_id AND a.month_year = strftime('%Y-%m', DATE(b.month_year || '-01', '+1 month'))

-- Join with A_Locations_Summary to get the actual country name
LEFT JOIN A_Locations_Summary AS loc
ON a.loc_id = loc.loc_id

-- Exclude the specified countries and filter for those above the global average
WHERE loc.location NOT IN (
    'Anguilla', 'Africa', 'Asia', 'Europe', 'European Union', 'Faeroe Islands', 
    'Falkland Islands', 'Gibraltar', 'Greenland', 'Hong Kong', 'Macao', 
    'Northern Cyprus', 'Oceania', 'Palestine', 'Pitcairn', 'Scotland', 
    'Sint Maarten (Dutch part)', 'Tokelau', 'Turks and Caicos Islands', 
    'World', 'North America', 'South America', 'Aruba', 'Bermuda', 
    'Bonaire, Sint Eustatius, and Saba', 'British Virgin Islands', 
    'Cayman Islands', 'Cook Islands', 'Curacao', 'England', 
    'French Polynesia', 'Guernsey', 'Isle of Man', 'Jersey', 
    'Montserrat', 'New Caledonia', 'Niue', 'Northern Ireland', 
    'Pitcairn Islands', 'Saint Helena', 'Taiwan', 'Timor', 
    'Wales', 'Wallis and Futuna'
)
AND ROUND(IFNULL(((a.monthly_total - IFNULL(b.monthly_total, 0)) * 100.0 / IFNULL(b.monthly_total, 1)), 0), 2) >
    (SELECT AVG((c.monthly_total - IFNULL(d.monthly_total, 0)) * 100.0 / IFNULL(d.monthly_total, 1))
     FROM (
         SELECT loc_id, 
                strftime('%Y-%m', date) AS month_year,
                SUM(daily_vaccinations) AS monthly_total
         FROM F_Vaccination_Daily_Data
         GROUP BY loc_id, strftime('%Y-%m', date)
     ) AS c
     LEFT JOIN (
         SELECT loc_id, 
                strftime('%Y-%m', date) AS month_year,
                SUM(daily_vaccinations) AS monthly_total
         FROM F_Vaccination_Daily_Data
         GROUP BY loc_id, strftime('%Y-%m', date)
     ) AS d 
     ON c.loc_id = d.loc_id AND c.month_year = strftime('%Y-%m', DATE(d.month_year || '-01', '+1 month'))
     WHERE c.month_year = strftime('%Y-%m', a.date)
    )

ORDER BY "Country Name", "Year", "Month";


    
-- Q3 --

SELECT 
    vt."Vaccine Type",
    loc.location AS Country,
    ROUND((vt.total_vaccine_vaccinations * 100.0 / ct.total_country_vaccinations), 2) AS "Percentage of Vaccine Type"
FROM 
    (SELECT 
         loc_id AS Country,
         vaccine AS "Vaccine Type",
         SUM(total_vaccinations) AS total_vaccine_vaccinations
     FROM 
         C_Vaccination_Manufacturers
     GROUP BY 
         loc_id, vaccine
    ) AS vt
JOIN 
    (SELECT 
         loc_id AS Country,
         SUM(total_vaccinations) AS total_country_vaccinations
     FROM 
         C_Vaccination_Manufacturers
     GROUP BY 
         loc_id
    ) AS ct 
ON vt.Country = ct.Country
JOIN 
    A_Locations_Summary loc 
ON vt.Country = loc.loc_id
WHERE 
    loc.location NOT IN (
        'Africa', 'Asia', 'Europe', 'European Union', 'Faeroe Islands', 
        'Falkland Islands', 'Gibraltar', 'Greenland', 'Hong Kong', 'Macao', 
        'Northern Cyprus', 'Oceania', 'Palestine', 'Pitcairn', 'Scotland', 
        'Sint Maarten (Dutch part)', 'Tokelau', 'Turks and Caicos Islands', 
        'World', 'North America', 'South America', 'Aruba', 'Bermuda', 
        'Bonaire, Sint Eustatius, and Saba', 'British Virgin Islands', 
        'Cayman Islands', 'Cook Islands', 'Curacao', 'England', 
        'French Polynesia', 'Guernsey', 'Isle of Man', 'Jersey', 
        'Montserrat', 'New Caledonia', 'Niue', 'Northern Ireland', 
        'Pitcairn Islands', 'Saint Helena', 'Taiwan', 'Timor', 
        'Wales', 'Wallis and Futuna'
    )
    AND (
        SELECT COUNT(*)
        FROM (
            SELECT 
                loc_id AS Country,
                vaccine AS "Vaccine Type",
                SUM(total_vaccinations) AS total_vaccine_vaccinations
            FROM 
                C_Vaccination_Manufacturers
            GROUP BY 
                loc_id, vaccine
        ) AS sub_vp
        JOIN 
            (SELECT 
                 loc_id AS Country,
                 SUM(total_vaccinations) AS total_country_vaccinations
             FROM 
                 C_Vaccination_Manufacturers
             GROUP BY 
                 loc_id
            ) AS sub_ct 
        ON sub_vp.Country = sub_ct.Country
        WHERE sub_vp.Country = vt.Country
          AND (sub_vp.total_vaccine_vaccinations * 100.0 / sub_ct.total_country_vaccinations) >= 
              (vt.total_vaccine_vaccinations * 100.0 / ct.total_country_vaccinations)
    ) <= 5
ORDER BY 
    loc.location, "Percentage of Vaccine Type" DESC;


-- Q4 --
SELECT 
    loc.location AS "Country Name",
    strftime('%Y-%m', g.date) AS "Month",
    details.source_name || ' (' || details.source_url || ')' AS "Source Name (URL)",
    IFNULL(SUM(g.total_vaccinations), 0) AS "Total Administered Vaccines"
FROM 
    G_Vaccination_Population_Total_Data AS g
JOIN 
    A_Locations_Summary AS loc ON g.loc_id = loc.loc_id
JOIN 
    B_Locations_Summary_Details AS details ON g.loc_id = details.loc_id 
                                          AND strftime('%Y-%m', g.date) = strftime('%Y-%m', details.last_observation_date)
WHERE 
    loc.location NOT IN (
        'Africa', 'Asia', 'Europe', 'European Union', 'Faeroe Islands', 
        'Falkland Islands', 'Gibraltar', 'Greenland', 'Hong Kong', 'Macao', 
        'Northern Cyprus', 'Oceania', 'Palestine', 'Pitcairn', 'Scotland', 
        'Sint Maarten (Dutch part)', 'Tokelau', 'Turks and Caicos Islands', 
        'World', 'North America', 'South America', 'Aruba', 'Bermuda', 
        'Bonaire, Sint Eustatius, and Saba', 'British Virgin Islands', 
        'Cayman Islands', 'Cook Islands', 'Curacao', 'England', 
        'French Polynesia', 'Guernsey', 'Isle of Man', 'Jersey', 
        'Montserrat', 'New Caledonia', 'Niue', 'Northern Ireland', 
        'Pitcairn Islands', 'Saint Helena', 'Taiwan', 'Timor', 
        'Wales', 'Wallis and Futuna'
    )
GROUP BY 
    loc.location,
    strftime('%Y-%m', g.date),
    details.source_name,
    details.source_url
ORDER BY 
    "Country Name" ASC, 
    "Month" DESC;
    


-- Q5 --

SELECT 
    a.date AS "Dates",
    
    -- Increment for United States
    (us.people_fully_vaccinated - COALESCE(prev_us.people_fully_vaccinated, 0)) AS "United States",
    
    -- Increment for China
    (cn.people_fully_vaccinated - COALESCE(prev_cn.people_fully_vaccinated, 0)) AS "China",
    
    -- Increment for Ireland
    (ie.people_fully_vaccinated - COALESCE(prev_ie.people_fully_vaccinated, 0)) AS "Ireland",
    
    -- Increment for India
    (inr.people_fully_vaccinated - COALESCE(prev_inr.people_fully_vaccinated, 0)) AS "India"

FROM 
    -- Selecting unique dates in the specified period
    (SELECT DISTINCT date FROM J_CN_IN_IE_US_Population_Total 
     WHERE date BETWEEN '2022-01-01' AND '2023-12-31') AS a

-- United States current and previous day join
LEFT JOIN J_CN_IN_IE_US_Population_Total AS us 
    ON a.date = us.date AND us.loc_id = 'USA'
LEFT JOIN J_CN_IN_IE_US_Population_Total AS prev_us 
    ON us.loc_id = prev_us.loc_id 
    AND prev_us.date = (SELECT MAX(date) FROM J_CN_IN_IE_US_Population_Total 
                        WHERE loc_id = 'USA' AND date < us.date)

-- China current and previous day join
LEFT JOIN J_CN_IN_IE_US_Population_Total AS cn 
    ON a.date = cn.date AND cn.loc_id = 'CHN'
LEFT JOIN J_CN_IN_IE_US_Population_Total AS prev_cn 
    ON cn.loc_id = prev_cn.loc_id 
    AND prev_cn.date = (SELECT MAX(date) FROM J_CN_IN_IE_US_Population_Total 
                        WHERE loc_id = 'CHN' AND date < cn.date)

-- Ireland current and previous day join
LEFT JOIN J_CN_IN_IE_US_Population_Total AS ie 
    ON a.date = ie.date AND ie.loc_id = 'IRL'
LEFT JOIN J_CN_IN_IE_US_Population_Total AS prev_ie 
    ON ie.loc_id = prev_ie.loc_id 
    AND prev_ie.date = (SELECT MAX(date) FROM J_CN_IN_IE_US_Population_Total 
                        WHERE loc_id = 'IRL' AND date < ie.date)

-- India current and previous day join
LEFT JOIN J_CN_IN_IE_US_Population_Total AS inr 
    ON a.date = inr.date AND inr.loc_id = 'IND'
LEFT JOIN J_CN_IN_IE_US_Population_Total AS prev_inr 
    ON inr.loc_id = prev_inr.loc_id 
    AND prev_inr.date = (SELECT MAX(date) FROM J_CN_IN_IE_US_Population_Total 
                         WHERE loc_id = 'IND' AND date < inr.date)

ORDER BY a.date;
