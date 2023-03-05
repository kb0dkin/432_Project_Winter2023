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
	LabReportDate                        string `json:"lab_report_date"`
	CasesTotal                           string `json:"cases_total"`
	DeathsTotal                          string `json:"deaths_total"`
	HospitalizationsTotal                string `json:"hospitalizations_total"`	
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
	trips := CSVSample("naz8-j4nc")

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

	stmt, err := db.Prepare(`INSERT INTO covid_19_daily_cases (lab_report_date, cases_total, deaths_total, hospitalizations_total) VALUES ($1, $2, $3, $4) ON CONFLICT (lab_report_date) DO UPDATE SET cases_total = $2, deaths_total = $3, hospitalizations_total = $4;`)
	if err != nil {
	log.Fatal(err)
	}
	defer stmt.Close()


	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip.LabReportDate, trip.CasesTotal, trip.DeathsTotal, trip.HospitalizationsTotal)
		count := 0
		if trip.LabReportDate != "" && trip.CasesTotal != "" && trip.DeathsTotal != "" && trip.HospitalizationsTotal != "" {
			_, err = stmt.Exec(			
				trip.LabReportDate,
				trip.CasesTotal,
				trip.DeathsTotal,
				trip.HospitalizationsTotal,
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted trip with ID %s\n", trip.LabReportDate)
			fmt.Printf("Count %d\n", count)
			count++
	}
}

}