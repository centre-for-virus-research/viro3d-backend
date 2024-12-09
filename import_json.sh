#!/usr/bin bash

echo "Importing JSON data..."
mongoimport --db viro3d --collection proteinstructures --file /data/import/proteinstructures.json --jsonArray
mongoimport --db viro3d --collection genome_coordinates --file /data/import/genome_coordinates.json --jsonArray
echo "JSON data imported."
