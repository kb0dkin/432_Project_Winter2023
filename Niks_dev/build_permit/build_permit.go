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
	ID string `json:"id"`
	Permit string `json:"permit_"`
	ApplicationStartDate string `json:"application_start_date"`
	IssueDate string `json:"issue_date"`
	CommunityArea string `json:"community_area"`
	Ward string `json:"ward"`
	Latitude string `json:"latitude"`
	Longitude string `json:"longitude"`

}





func CSVSample(data_set string) Trip {
	APP_TOKEN := "8nxBA5pgg7aPQ4fDbf4wj8BfM"
	url_format := fmt.Sprintf("https://data.cityofchicago.org/resource/%s", data_set)
	sodareq := soda.NewGetRequest(url_format, APP_TOKEN)
	sodareq.Format = "json"	
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
	//Get everything after 01/01/2022
	
	// Get a sample of taxi trips from the Socrata API from today
	trips := CSVSample("ydr8-5enu")

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

	stmt, err := db.Prepare(`INSERT INTO build_permit (id, permit_, application_start_date, issue_date, community_area, ward, latitude, longitude) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT (id) DO NOTHING`)
	if err != nil {
	log.Fatal(err)
	}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip.ID, trip.Permit, trip.ApplicationStartDate, trip.IssueDate, trip.CommunityArea, trip.Ward)
		count := 0
		if trip.ID != "" && trip.Permit != "" && trip.ApplicationStartDate != "" && trip.IssueDate != "" && trip.CommunityArea != "" && trip.Ward != "" && trip.Latitude != "" && trip.Longitude != "" {
			_, err = stmt.Exec(			
				trip.ID,
				trip.Permit,
				trip.ApplicationStartDate,
				trip.IssueDate,
				trip.CommunityArea,
				trip.Ward,
				trip.Latitude,
				trip.Longitude,
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted trip with ID %s\n", trip.ID)
			fmt.Printf("Count %d\n", count)
			count++
	}
}

}