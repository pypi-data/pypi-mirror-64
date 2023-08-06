# ReGraph

Graph rewriting and graph-based knowledge representation library. Documentation is available at http://dev.executableknowledge.org/ReGraph.

## About project

The **ReGraph** Python library is a generic framework for modelling graph-based systems. In this context models are viewed as graphs and graph transformations --- as a tool to describe both the system evolution and the model evolution [read more about the approach](http://link.springer.com/chapter/10.1007%2F978-3-540-30203-2_30). 

ReGraph provides various utilities for graph rewriting which can be used for modelling the evolution of a system represented by a graph subject to rewriting. The rewriting functionality is based on the sesqui-pushout rewriting procedure [7]. In addition, the library enables a user to define a typing for models (graphs) that gives specifications for the structure of the models. This later functionality allows both to preserve the specified structure during rewriting and to propagate the changes to the specifications up to the models.

**ReGraph** contains a collection of utilities for rewriting graphs and hierarchies of graphs. It supports two backends: [NetworkX](https://networkx.github.io/) graph objects and on [Neo4j](https://neo4j.com/) property graphs stored in a graph database.

## Environment configs 

### Requirement

The required `Python 3` packages are given inside the requirements.txt file

To avoid manual installation and to easily set up development environment you may consider following the instructions below:

### (Optional ) Setup virtual environment

Create a new virtual environment
```
virtualenv venv -p path/to/your/python3
```

To activate the environment
```
source venv/bin/activate
```

## Installation

In order to install the **ReGraph** library you have to clone this repository using SSH
```
git clone git@github.com:Kappa-Dev/ReGraph.git
```
or using HTTPS
```
https://github.com/Kappa-Dev/ReGraph.git
```
Install the library with
```
python setup.py install
```

### Neo4j installation and configuration

If you want to use the Neo4j-based backend of ReGraph, you need to install the Neo4j database (see installation [instructions](https://neo4j.com/docs/operations-manual/current/installation/)).

Moreover, ReGraph uses the APOC Neo4j plugin, currently not included in the community edition. To install the plugin see the [instructions](https://github.com/neo4j-contrib/neo4j-apoc-procedures/blob/4.0/readme.adoc).

ReGraph uses [Neo4j Bolt Driver for Python](https://neo4j.com/docs/api/python-driver/current/#), therefore, having set up your database, you need to provide to ReGraph's API the address of the bolt server (for example, `bolt://127.0.0.1:7687`) and your credentials for connecting the database (i.e. user and password).



## Run tests

### Nosetests
```
nosetests -v -s
```

