#!/bin/bash
mongoimport --db viro3d --collection proteinstructures --file /data/import/proteinstructures.json --jsonArray
mongoimport --db viro3d --collection genome_coordinates --file /data/import/genome_coordinates.json --jsonArray