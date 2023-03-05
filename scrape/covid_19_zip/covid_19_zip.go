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
	RowID                           string `json:"row_id"`
	ZipCode                         string `json:"zip_code"`
	WeekNumber                      string `json:"week_number"`
	WeekStart                       string `json:"week_start"`
	CasesWeekly                     string `json:"cases_weekly"`
	CaseRateCumulative              string `json:"case_rate_cumulative"`
	DeathsWeekly                    string `json:"deaths_weekly"`
	DeathRateWeekly                 string `json:"death_rate_weekly"`
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
	trips := CSVSample("yhhz-zm2v")

	host := "34.134.248.227"
    port := 5432
    user := "postgres"
    password := "432"
    dbname := "bronze"
    connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)

	// Open a new database connection
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        panic(err)
    }
    defer db.Close()

	stmt, err := db.Prepare(`INSERT INTO covid_19_zip (row_id, zip_code, week_number, week_start, cases_weekly, case_rate_cumulative, deaths_weekly, death_rate_weekly) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`)
	if err != nil {
	log.Fatal(err)
	}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip.RowID)
		count := 0
		if trip.RowID != "" && trip.ZipCode != "" && trip.WeekNumber != "" && trip.WeekStart != "" && trip.CasesWeekly != "" && trip.CaseRateCumulative != "" && trip.DeathsWeekly != "" && trip.DeathRateWeekly != ""{
			_, err = stmt.Exec(			
				trip.RowID,
				trip.ZipCode,
				trip.WeekNumber,
				trip.WeekStart,
				trip.CasesWeekly,
				trip.CaseRateCumulative,
				trip.DeathsWeekly,
				trip.DeathRateWeekly,
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted trip with ID %s\n", trip.RowID)
			fmt.Printf("Count %d\n", count)
			count++
	}
}

}