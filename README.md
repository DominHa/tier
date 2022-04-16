# Tier Vehicle Cluster API Challenge
Let's do this!
## prerequisites
- docker and docker compose

To set up the local docker stack, cd into the projects/localdev/ directory and run start.sh script.
(Use sudo if you haven't given the user permissions to start docker)
```bash
cd projects/localdev/
sudo ./start.sh
```
This script will setup the local docker container running the api. Once it is up, open a browser and nagivate to:
```
locahost:8080/v1/docs
```
You should be able to see the Swagger docs

The /v1/vehicles endpoint will return a list of vehicles. 

There is a default limit but it is an optional parameter. The limit is in place just to make querying through Swagger a bit smoother. If you want to see an unlimited amount of vehicles you can skip it. 

The following parameters are available:
- maximum_distance_from_user_m :  Will filter out bikes that are too far away for you. You will need to provide a user location in the body to use this. 
- estimated_journey_distance_m : Will filter out vehicles that don't have enough charge left to take you where you need to go. You will need to provide a user location in the body to use this. 
- vehicle_type  : for now these are either "escooter_paris" or "ebike_paris"
- only_find_available: Some vehicles are either already reserved or they are disabled. If set to true this will filter those out.
- limit - a limit to the number of vehicles returned.

For the Eiffel Tower (which I've been using for manual tests):
``` json
{
  "user_location_coordinates": [
    "48.8584", "2.2945"
  ]
}
```

## LOCAL DEV

Move into the projects/localdev directory and create a virtualenv. You can use any virtualenv tool you like, just make sure you activate the environment before installing things.
```bash
virtualenv .localvenv

source .localvenv/bin/activate
```
Install the requirements.txt file from the project/shared directory
```bash
pip install -r api_requirements.txt
```

To run the tests run
``` bash
pytest
```

Enjoy!
