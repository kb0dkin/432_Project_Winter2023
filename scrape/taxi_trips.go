package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/SebastiaanKlippert/go-soda"
	_ "github.com/lib/pq"
)

//https://data.cityofchicago.org/resource/wrvz-psew.json?$where=trip_miles > 0.1

//import API TOKEN

//create a struct to hold the data

type Trip []struct {
	TripID                  string `json:"trip_id"`
	TaxiID                  string `json:"taxi_id"`
	TripSeconds             string `json:"trip_seconds"`
	TripMiles               string `json:"trip_miles"`
	PickupCentroidLatitude  string `json:"pickup_centroid_latitude,omitempty"`
	PickupCentroidLongitude string `json:"pickup_centroid_longitude,omitempty"`
	DropoffCentroidLatitude  string `json:"dropoff_centroid_latitude,omitempty"`
	DropoffCentroidLongitude string `json:"dropoff_centroid_longitude,omitempty"`
	PickupCommunityArea     string `json:"pickup_community_area,omitempty"`
	DropoffCommunityArea     string `json:"dropoff_community_area,omitempty"`
}





func CSVSample(data_set string, query string) Trip {
	APP_TOKEN := "8nxBA5pgg7aPQ4fDbf4wj8BfM"
	url_format := fmt.Sprintf("https://data.cityofchicago.org/resource/%s", data_set)
	sodareq := soda.NewGetRequest(url_format, APP_TOKEN)
	sodareq.Format = "json"
	sodareq.Query.Where = query
	sodareq.Query.Limit = 1000



	// Gets the response
	//wait 1 second
	time.Sleep(1 * time.Second)
	resp, err := sodareq.Get()
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// Decodes the response
	var trips Trip
	err = json.NewDecoder(resp.Body).Decode(&trips)
	if err != nil {
		log.Fatal(err)
	}






	return trips


}

// main

func main() {
	// Get today's date
	//02/01/2023 12:00:00 AM
	//https://data.cityofchicago.org/api/id/wrvz-psew.json?$query=select *, :id order by `trip_start_timestamp` asc limit 100
	//Get everything after 2023-01-01
	
	where_statement := "trip_start_timestamp > '2022-01-01T00:00:00.000'"


	// Get a sample of taxi trips from the Socrata API from today
	trips := CSVSample("wrvz-psew", where_statement)

	host := "localhost"
    port := 5432
    user := "postgres"
    password := "password"
    dbname := "mydatabase"
    connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)

	// Open a new database connection
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        panic(err)
    }
    defer db.Close()

	// Prepare a SQL statement to insert a new row into the 'taxi_trips' table
	stmt, err := db.Prepare(`INSERT INTO taxi_trips (    
    trip_id,
    taxi_id,
    trip_seconds,
    trip_miles,
    community_area_pickup,
	dropoff_community_area
	) VALUES ($1, $2, $3, $4, $5, $6)
	ON CONFLICT (trip_id) DO NOTHING`)
	if err != nil {
    log.Fatal(err)
		}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip.TripID)
		count := 0
		if trip.TripID != "" && trip.TripSeconds != "" && trip.TripMiles != "" && trip.PickupCommunityArea != "" && trip.DropoffCommunityArea != "" && trip.TaxiID != "" {
			_, err = stmt.Exec(			
				trip.TripID,
				trip.TaxiID,
				trip.TripSeconds,
				trip.TripMiles,
				trip.PickupCommunityArea,
				trip.DropoffCommunityArea,
				
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted trip with ID %s\n", trip.TripID)
			fmt.Printf("Count %d\n", count)
			count++
	}
}

}