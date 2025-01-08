# Viro3D API

Viro3D is a comprehensive, searchable and browsable database of viral protein structure predictions, containing over 85,000 structural models from more than 4,400 human and animal viruses. This is the API for interfacing with the data.

### <a href="https://github.com/centre-for-virus-research/viro3d-frontend">Frontend Code</a>

# Tech Stack
```FastAPI```
```MongoDB```
```ncbi blast+```
```pytest```

# Running Manually

### Prerequisites

You'll need python@3.6 or later, mongod@7.0.15 or later and ncbi blast+ 2.12.0.

### Installing

Create a python virtual environment in the project with the following command (optional)

```python -m venv /path/to/new/virtual/environment```

Run the following command to install all the project dependencies

```pip install```

Ensure you have a local mongodb install running with the following command (MacOS & Linux):

```systemctl start mongod```

Create the Viro3D database and its collections:

```mongoimport --db viro3d --collection proteinstructures --file <PATH_TO>/protein_structures.json --jsonArray && mongoimport --db viro3d --collection genome_coordinates --file <PATH_TO>/genome_coordinates.json --jsonArray && mongoimport --db viro3d --collection clusters --file <PATH_TO>/clusters.json --jsonArray```

Create the blastp database:

```makeblastdb -in <PATH_TO_YOUR_FASTA_FILE>/viro3d_seq_db.fas -dbtype prot -out viro3d_blast_db```

### Running Locally

Enter to run the app in development mode:

```fastapi dev app/main.py```

### Running Tests

Enter to run the tests:

```cd tests && pytest```

# Running With Docker

### Prerequisites

You'll need Docker@27.3.1. (if you use an earlier version, ensure docker-compose is also installed seperately).

Ensure that the structural models (pdbs and mmCIF) and graph data are one step outside the project directory, e.g:

```.
├── static
│   ├── graph_data
│   └── structural_models
├── viro3d-backend
│   ├── app
│   ├── database
│   ├── tests
│   └── venv
```

Run the command:

```docker compose up```

To stop the container, run:

```docker compose down```

