## sam-eval

I figured I might as well come up with a use case for getting familiar with AWS serverless application model, so I decided to try and find some amount of correlation in the dataset I collected a few years back.
- There are about 20 entries in the dataset, stored as flat json in S3
- the `spot_` keys represent locations on the basketball court, and the value for each is the amount made out of 4 attempts
- the `temp` is the recorded temperature at the time, in Farenheit
- so in this example, 1 shot out of 4 was made from `spot_1` and the temperature outside was 93, yikes
```json
    {
        "spot_1": "1", 
        "spot_2": "2", 
        "spot_3": "1", 
        "spot_4": "0", 
        "spot_5": "1", 
        "spot_6": "1", 
        "spot_7": "1", 
        "spot_8": "1", 
        "spot_9": "4", 
        "spot_10": "2", 
        "spot_11": "1",
        "temp": "93",
        "date": "2021-06-11",
        "time": "12:9:25"
    }
```