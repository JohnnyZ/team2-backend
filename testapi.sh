#!/bin/bash
# Call this script with at least 1 parameter, for example
# ./testapi apiname arg1 arg2

if [ "$1" = "create_user" ]; then 
    echo "Creating User"
    echo 'curl -v -H "Content-Type: application/json" -X POST --data '{"birthday" : "2015-03-30", "gender": "1", "first_name": "John", "last_name": "Doe", "email" : "goooch_attack\$2@catfacts.co", "username": "lotus_user\$2", "raw_password": "password"}' https://secure-headland-8362.herokuapp.com/api/v1/create_user/'
    curl -v -H "Content-Type: application/json" -X POST --data '{"birthday" : "2015-03-30", "gender": "1", "first_name": "John", "last_name": "Doe", "email" : "goooch_attack\$2@catfacts.co", "username": "lotus_user\$2", "raw_password": "password"}' https://secure-headland-8362.herokuapp.com/api/v1/create_user/
else
    echo "$1 isn't a valid api"  
fi;