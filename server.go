package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Cafeteria struct {
	CoverName   string `json:"cover_name"`
	Endpoint    string `json:"endpoint"`
	IsClosed    bool   `json:"is_closed"`
	Restaurants []struct {
		Breakfast []string `json:"breakfast"`
		Dinner    []string `json:"dinner"`
		Endpoint  string   `json:"endpoint"`
		LateNight []string `json:"late_night"`
		Lunch     []string `json:"lunch"`
		Name      string   `json:"name"`
	} `json:"restaurants"`
	UniqueName string `json:"unique_name"`
}

func loadMenuJson() (cafeteriaMap map[string]Cafeteria) {
	b, err := ioutil.ReadFile("menus.json")
	if err != nil {
		fmt.Println(err)
	}

	var data []Cafeteria
	if err = json.Unmarshal(b, &data); err != nil {
		panic(err)
	}

	// Build the map of caf name to caf object
	cafeteriaMap = make(map[string]Cafeteria)
	for i := range data {
		rest := data[i]
		//fmt.Println(rest.CoverName)
		cafeteriaMap[rest.UniqueName] = rest
	}

	/*
		Sample marshalling.

			testRest := data[4]
			b, err = json.Marshal(testRest)
			if err = ioutil.WriteFile("test.json", b, 0644); err != nil {
				panic(err)
			}
	*/

	return
}

type MenuHeaders struct {
	CafeteriaName string `json:"cafeteria_name"`
}

func serveCafeteriaJson(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	if r.Method == "POST" {
		// check if name was in the body and respond with 402 if not
		if r.Body == nil {
			http.Error(w, "Empty request body.", 402)
			return
		}

		// extract the cafeteria name from the request
		var requestHeaders MenuHeaders
		if err := json.NewDecoder(r.Body).Decode(&requestHeaders); err != nil {
			fmt.Println(err)
			return
		}

		// TODO: Handle invalid cafeteria name
		cafeteria := currentCafeMap[requestHeaders.CafeteriaName]
		json.NewEncoder(w).Encode(cafeteria)
	}

}

var currentCafeMap map[string]Cafeteria

func main() {
	// this will be used to serve up the data
	currentCafeMap = loadMenuJson()

	// setup http server and serve the cafes
	http.HandleFunc("/menu", serveCafeteriaJson)
	http.ListenAndServe(":8000", nil)
}
