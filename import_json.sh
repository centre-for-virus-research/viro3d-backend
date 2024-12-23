#!/usr/bin bash

echo "Importing JSON data..."
mongoimport --db viro3d --collection proteinstructures --file /data/import/protein_structures.json --jsonArray
mongoimport --db viro3d --collection genome_coordinates --file /data/import/genome_coordinates.json --jsonArray
mongoimport --db viro3d --collection clusters --file /data/import/clusters.json --jsonArray
echo "JSON data imported."