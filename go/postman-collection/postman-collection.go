package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

func readJson() map[string]interface{} {
	jsonFile, err := os.Open("postman_collection.json")
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
		return nil
	}

	fmt.Println("Successfully Opened postman_collection.json")
	byteValue, _ := ioutil.ReadAll(jsonFile)

	var result map[string]interface{}
	json.Unmarshal([]byte(byteValue), &result)
	return result
}

func main() {
	var result = readJson()
	fmt.Println(result)
}
