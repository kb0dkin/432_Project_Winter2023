-- connect to silver
\c silver;

-- taxi covid -- 
--    import data from bronze taxi table
WITH (reverse_geocode(POINT(t_t.dropoff_centroid_latitude,t_t.dropoff_centroid_longitude)).addy[1]) as addr
INSERT INTO taxi_covid
SELECT t_t.trip_start_timestamp as ride_date, c_z.cases_weekly as covid_rate, c_z.zip_code as zip_end, COUNT(t_t.trip_id)
FROM bronze.covid_19_zip as c_z, bronze.taxi_trips as t_t
JOIN ON t_t.week_number = WEEK(c_z.ride_date)
WHERE c_z.zip_code = 