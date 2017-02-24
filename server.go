package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"
)

type Cafeteria struct {
	CoverName   string `json:"cover_name"`
	Endpoint    string `json:"endpoint"`
	IsClosed    bool   `json:"is_closed"`
	Restaurants []struct {
		Breakfast []string `json:"breakfast"`
		Dinner    []string `json:"dinner"`
		Endpoint  string   `json:"endpoint"`
		IsClosed  bool     `json:"is_closed"`
		LateNight []string `json:"late_night"`
		Lunch     []string `json:"lunch"`
		Name      string   `json:"name"`
	} `json:"restaurants"`
	UniqueName string `json:"unique_name"`
}

type FoodItem struct {
	Allergens []string `json:"allergens"`
	Ingredients []string `json:"ingredients"`
	MetricToValueNutritionFacts struct {
			  Calories string `json:"calories"`
			  CaloriesFromFat int `json:"calories_from_fat"`
			  Cholesterol string `json:"cholesterol"`
			  DietaryFiber string `json:"dietary_fiber"`
			  Protein string `json:"protein"`
			  SaturatedFat string `json:"saturated_fat"`
			  Sodium string `json:"sodium"`
			  Sugars string `json:"sugars"`
			  TotalCarbohydrate string `json:"total_carbohydrate"`
			  TotalFat string `json:"total_fat"`
		  } `json:"metric_to_value_nutrition_facts"`
	Name string `json:"name"`
	Number int `json:"number"`
	NutritionHTML string `json:"nutrition_html"`
	ServingSize string `json:"serving_size"`
	UniqueName string `json:"unique_name"`
}

type CafeAPIResponse struct {
	FoodItems []FoodItem `json:"food_items"`
	Restaurants []struct {
		FoodNumbers []int `json:"food_numbers"`
		Number int `json:"number"`
	} `json:"restaurants"`
}

func loadMenuJson() (map[string]Cafeteria, []Cafeteria) {
	b, err := ioutil.ReadFile("menus.json")
	if err != nil {
		fmt.Println(err)
	}

	var data []Cafeteria
	if err = json.Unmarshal(b, &data); err != nil {
		panic(err)
	}

	// Build the map of caf name to caf object
	cafeteriaMap := make(map[string]Cafeteria)
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

	return cafeteriaMap, data
}

func loadFoodItemJson() (map[string]FoodItem, []FoodItem){
	b, err := ioutil.ReadFile("food_items.json")
	if err != nil {
		panic(err)
	}

	var data []FoodItem
	if err = json.Unmarshal(b, &data); err != nil {
		panic(err)
	}

	// Build the map of caf name to caf object
	foodMap := make(map[string]FoodItem)
	for i := range data {
		food := data[i]
		fmt.Println(food.UniqueName)
		foodMap[food.UniqueName] = food
	}

	/*
		Sample marshalling.

			testRest := data[4]
			b, err = json.Marshal(testRest)
			if err = ioutil.WriteFile("test.json", b, 0644); err != nil {
				panic(err)
			}
	*/

	return foodMap, data
}

type MenuHeaders struct {
	CafeteriaName string `json:"cafeteria_name"`
}

func serveCafeteriaJson(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	fmt.Println("DEBUG: (serveCafeteriaJson)", time.Now(), " - Request recieved from host: ", r.RemoteAddr)

	if r.Method == "POST" {
		// check if name was in the body and respond with 402 if not
		if r.Body == nil {
			//http.error(w, "empty request body.", 402)
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
		fmt.Println("DEBUG: (serveCafeteriaJson) - Response written for host: " + r.RemoteAddr)
	}
}

func serveAllCafeteriaJson(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	fmt.Println("DEBUG: (serveAllCafeteriaJson)", time.Now(), " - Request recieved from host: ", r.RemoteAddr)
	if r.Method == "GET" {
		json.NewEncoder(w).Encode(currentCafeArray)
		fmt.Println("DEBUG: (serveAllCafeteriaJson) - Response written for host: " + r.RemoteAddr)
	}
}

type FoodItemHeaders struct {
	FootItemName string `json:"food_item_name"`
}

func serveFoodItemJson(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	fmt.Println("DEBUG: (serveFoodItemJson)", time.Now(), " - Request recieved from host: ", r.RemoteAddr)

	if r.Method == "POST" {
		// check if name was in the body and respond with 402 if not
		if r.Body == nil {
			//http.error(w, "empty request body.", 402)
			return
		}

		// extract the cafeteria name from the request
		var requestHeaders FoodItemHeaders
		//fmt.Println("Body: ", "'", r.Body, "'")
		if err := json.NewDecoder(r.Body).Decode(&requestHeaders); err != nil {
			fmt.Println(err)
			return
		}

		// TODO: Handle invalid cafeteria name
		foodItem := currentFoodItemMap[requestHeaders.FootItemName]
		fmt.Println("DEBUG: (serveFoodItemJson) - food item = ", "'" + requestHeaders.FootItemName + "'")
		fmt.Println("DEBUG: (serveFoodItemJson) - found food item = ", "'" + foodItem.UniqueName+ "'")
		json.NewEncoder(w).Encode(foodItem)
		fmt.Println("DEBUG: (serveFoodItemJson) - Response written for host: " + r.RemoteAddr)
	}
}


func serveAllFoodItemJson(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	fmt.Println("DEBUG: (serveAllFoodItemJson)", time.Now(), " - Request recieved from host: ", r.RemoteAddr)
	if r.Method == "GET" {
		json.NewEncoder(w).Encode(currentFoodItemArray)
		fmt.Println("DEBUG: (serveAllCafeteriaJson) - Response written for host: " + r.RemoteAddr)
	}
}

var currentCafeMap map[string]Cafeteria
var currentCafeArray []Cafeteria
var currentFoodItemMap map[string]FoodItem
var currentFoodItemArray []FoodItem

func main() {
	// this will be used to serve up the data
	currentCafeMap, currentCafeArray = loadMenuJson()
	currentFoodItemMap, currentFoodItemArray = loadFoodItemJson()

	// setup http server and serve the cafes
	http.HandleFunc("/menu/cafeteria", serveCafeteriaJson)
	http.HandleFunc("/menu/all_cafeterias", serveAllCafeteriaJson)
	http.HandleFunc("/nutrition/all_foods", serveAllFoodItemJson)
	http.HandleFunc("/nutrition/food", serveFoodItemJson)
	http.ListenAndServe(":8000", nil)
}
