const express = require('express');
const app = express(); // Creates an express application

app.use(express.json()); // Parses incoming requests with JSON payloads
app.use(express.urlencoded({extended: true})); // Parses incoming requests with urlencoded payloads

car_count = null;

app.get("/car-count", (req, res) => {
    if (car_count == null)
        return;

    console.log(car_count);
    res.status(200).json({ "CART_COUNT" : car_count })
});

app.post("/car-count/:cars", (req, res) => {
    cars = req.params.cars;
    
    if (cars == null)
        return;

    car_count = cars;
    
    res.status(200).json("success")
});

module.exports = app;