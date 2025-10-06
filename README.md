# Daimler Dealership Competition Simulation

This repository contains a simple agent-based simulation focused on how a Daimler truck dealership competes with rival dealerships from Volvo and PACCAR. The model mixes manufacturer attributes, dealership capabilities, and market behavior to estimate monthly sales and overall market share.

## Features

- Manufacturer and dealership data models capturing pricing, technology, service quality, and local relationships.
- Market dynamics including baseline demand, economic volatility, and customer preferences.
- Preconfigured scenario for Daimler versus Volvo and PACCAR competitors with a command line interface.

## Usage

Run the simulation for 12 months with a deterministic seed:

```bash
python -m simulation.main --months 12 --seed 42
```

Optionally, write the summary to a JSON file:

```bash
python -m simulation.main --months 18 --seed 7 --output results.json
```

The command prints a JSON summary of total sales and market share for each dealership.

## Extending the Model

- Adjust manufacturer and dealership parameters in `simulation/scenario.py` to explore alternate strategies.
- Modify weights and demand assumptions in `simulation/market.py` for different economic conditions.
- Swap out the preconfigured scenario by importing the package in your own scripts.

