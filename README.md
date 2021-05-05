# TruSTAR Engineering : Technical challenge

Python script to read from forked GitHub repository folder (cti/enterprise-attack/attack-pattern)
all the json files, and extract from each one of them the following properties to be displayed:
- id
- objects[0].name
- objects[0].kill_chain_phases

## Prerequisites
Run the following commands:
```
git clone https://github.com/jmvd07/trustar.git
cd trustar
pip install requirements.txt
python trustar_engineering.py
```

## Script execution
Run the following command:
```
python trustar_engineering.py
```

## Running unit test
Run the following command:
```
python test_trustar_engineering.py
```
