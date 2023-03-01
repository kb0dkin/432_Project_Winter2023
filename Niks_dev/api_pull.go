package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/SebastiaanKlippert/go-soda"
	_ "github.com/lib/pq"
)

//https://data.cityofchicago.org/resource/wrvz-psew.json?$where=trip_miles > 0.1

//import API TOKEN

//create a struct to hold the data

type Trip []struct {
	Company                 string `json:"company"`
	DropoffCensusTract      string `json:"dropoff_census_tract,omitempty"`
	DropoffCentroidLatitude string `json:"dropoff_centroid_latitude,omitempty"`
	DropoffCentroidLocation struct {
		Coordinates []float64 `json:"coordinates"`
		Type        string    `json:"type"`
	} `json:"dropoff_centroid_location,omitempty"`
	DropoffCentroidLongitude string `json:"dropoff_centroid_longitude,omitempty"`
	DropoffCommunityArea     string `json:"dropoff_community_area,omitempty"`
	Extras                   string `json:"extras"`
	Fare                     string `json:"fare"`
	PaymentType              string `json:"payment_type"`
	PickupCensusTract        string `json:"pickup_census_tract,omitempty"`
	PickupCentroidLatitude   string `json:"pickup_centroid_latitude,omitempty"`
	PickupCentroidLocation   struct {
		Coordinates []float64 `json:"coordinates"`
		Type        string    `json:"type"`
	} `json:"pickup_centroid_location,omitempty"`
	PickupCentroidLongitude string `json:"pickup_centroid_longitude,omitempty"`
	PickupCommunityArea     string `json:"pickup_community_area,omitempty"`
	TaxiID                  string `json:"taxi_id"`
	Tips                    string `json:"tips"`
	Tolls                   string `json:"tolls"`
	TripEndTimestamp        string `json:"trip_end_timestamp"`
	TripID                  string `json:"trip_id"`
	TripMiles               string `json:"trip_miles"`
	TripSeconds             string `json:"trip_seconds"`
	TripStartTimestamp      string `json:"trip_start_timestamp"`
	TripTotal               string `json:"trip_total"`
}





func CSVSample(data_set string, query string) Trip {
	APP_TOKEN := os.Getenv("cqh5tqp0euzwjliw0si085ncm")
	url_format := fmt.Sprintf("https://data.cityofchicago.org/resource/%s", data_set)
	sodareq := soda.NewGetRequest(url_format, APP_TOKEN)
	sodareq.Format = "json"
	sodareq.Query.Where = query
	sodareq.Query.Limit = 10



	// Gets the response
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
	trips := CSVSample("wrvz-psew", "trip_miles > 10")

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
    company,
    dropoff_census_tract,
    dropoff_centroid_latitude,
    dropoff_centroid_location,
    dropoff_centroid_longitude,
    dropoff_community_area,
    extras,
    fare,
    payment_type,
    pickup_census_tract,
    pickup_centroid_latitude,
    pickup_centroid_location,
    pickup_centroid_longitude,
    pickup_community_area,
    taxi_id,
    tips,
    tolls,
    trip_end_timestamp,
    trip_id,
    trip_miles,
    trip_seconds,
    trip_start_timestamp,
    trip_total
	) VALUES ($1, $2::text, $3::float, $4::point, $5::float, $6::int, $7::float, $8::float, $9::text, $10::text, $11::float, $12::point, $13::float, $14::int, $15::text, $16::float, $17::float, $18::timestamp, $19::text, $20::float, $21::int, $22::timestamp, $23::float)`)
	if err != nil {
    log.Fatal(err)
		}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		_, err = stmt.Exec(
			trip.Company,
			trip.DropoffCensusTract,
			trip.DropoffCentroidLatitude,
			trip.DropoffCentroidLocation,
			trip.DropoffCentroidLongitude,
			trip.DropoffCommunityArea,
			trip.Extras,
			trip.Fare,
			trip.PaymentType,
			trip.PickupCensusTract,
			trip.PickupCentroidLatitude,
			trip.PickupCentroidLocation,
			trip.PickupCentroidLongitude,
			trip.PickupCommunityArea,
			trip.TaxiID,
			trip.Tips,
			trip.Tolls,
			trip.TripEndTimestamp,
			trip.TripID,
			trip.TripMiles,
			trip.TripSeconds,
			trip.TripStartTimestamp,
			trip.TripTotal,
		)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("Inserted trip with ID %s\n", trip.TripID)
	}
}