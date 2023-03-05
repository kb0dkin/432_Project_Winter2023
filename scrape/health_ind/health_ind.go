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
	CommunityArea string `json:"community_area"`
	CommunityAreaName string `json:"community_area_name"`
	BelowPovertyLevel string `json:"below_poverty_level"`
	NoHighSchoolDiploma string `json:"no_high_school_diploma"`
	PerCapitaIncome string `json:"per_capita_income"`
	Unemployment string `json:"unemployment"`

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
	trips := CSVSample("iqnk-2tcu")

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




	
	stmt, err := db.Prepare(`INSERT INTO health_ind (community_area, community_area_name, below_poverty_level, no_high_school_diploma, per_capita_income, unemployment) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING`)
	if err != nil {
	log.Fatal(err)
	}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip)
		count := 0
		if trip.CommunityArea != "" && trip.CommunityAreaName != "" && trip.BelowPovertyLevel != "" && trip.NoHighSchoolDiploma != "" && trip.PerCapitaIncome != "" && trip.Unemployment != ""{
			_, err = stmt.Exec(			
				trip.CommunityArea,
				trip.CommunityAreaName,
				trip.BelowPovertyLevel,
				trip.NoHighSchoolDiploma,
				trip.PerCapitaIncome,
				trip.Unemployment,
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted trip with ID %s\n", trip.CommunityArea)
			fmt.Printf("Count %d\n", count)
			count++
	}
}

}