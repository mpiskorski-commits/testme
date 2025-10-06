"""Preconfigured scenario modelling Daimler vs competitors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .entities import Dealership, Manufacturer, TruckModel
from .market import Market, MarketParameters


@dataclass
class SimulationResult:
    months: int
    sales_history: List[dict]

    def summary(self) -> dict:
        aggregated: dict[str, float] = {}
        for month in self.sales_history:
            for dealer, sales in month.items():
                aggregated[dealer] = aggregated.get(dealer, 0.0) + sales
        total = sum(aggregated.values()) or 1.0
        share = {dealer: sales / total for dealer, sales in aggregated.items()}
        return {"total_sales": aggregated, "market_share": share}


class DaimlerDealershipScenario:
    """Builds a simulation focused on Daimler competing with other OEMs."""

    def __init__(self, months: int = 12, seed: int | None = None, parameters: MarketParameters | None = None) -> None:
        self.months = months
        self.seed = seed
        self.parameters = parameters or MarketParameters()

    def _build_manufacturers(self) -> List[Manufacturer]:
        daimler = Manufacturer(
            name="Daimler Trucks",
            reputation=0.82,
            innovation=0.8,
            service_network=0.85,
            marketing_power=0.75,
            models=[
                TruckModel("Actros", "long-haul", 135000, 0.78, 0.82, 0.88),
                TruckModel("Atego", "distribution", 95000, 0.82, 0.75, 0.83),
                TruckModel("eActros", "electric", 220000, 0.95, 0.9, 0.8),
            ],
        )

        volvo = Manufacturer(
            name="Volvo Trucks",
            reputation=0.79,
            innovation=0.77,
            service_network=0.8,
            marketing_power=0.7,
            models=[
                TruckModel("FH16", "long-haul", 138000, 0.76, 0.79, 0.86),
                TruckModel("FM", "distribution", 97000, 0.8, 0.76, 0.84),
                TruckModel("FE Electric", "electric", 215000, 0.92, 0.85, 0.78),
            ],
        )

        paccar = Manufacturer(
            name="PACCAR",
            reputation=0.75,
            innovation=0.72,
            service_network=0.78,
            marketing_power=0.68,
            models=[
                TruckModel("Kenworth T680", "long-haul", 133000, 0.74, 0.74, 0.82),
                TruckModel("Peterbilt 579", "distribution", 96000, 0.78, 0.73, 0.81),
                TruckModel("Peterbilt 579EV", "electric", 210000, 0.9, 0.82, 0.77),
            ],
        )

        return [daimler, volvo, paccar]

    def _build_dealerships(self, manufacturers: List[Manufacturer]) -> List[Dealership]:
        daimler_dealer = Dealership(
            name="StarLine Daimler",
            manufacturer=manufacturers[0],
            local_relationships=0.88,
            salesforce=0.83,
            inventory={model.name: 30 for model in manufacturers[0].models},
            price_adjustment=-0.03,
            marketing_spend=0.12,
            service_quality=0.87,
            loyalty_program=True,
        )

        volvo_dealer = Dealership(
            name="Northway Volvo",
            manufacturer=manufacturers[1],
            local_relationships=0.8,
            salesforce=0.78,
            inventory={model.name: 28 for model in manufacturers[1].models},
            price_adjustment=-0.015,
            marketing_spend=0.1,
            service_quality=0.82,
            loyalty_program=True,
        )

        paccar_dealer = Dealership(
            name="Frontier PACCAR",
            manufacturer=manufacturers[2],
            local_relationships=0.76,
            salesforce=0.75,
            inventory={model.name: 26 for model in manufacturers[2].models},
            price_adjustment=-0.01,
            marketing_spend=0.08,
            service_quality=0.8,
            loyalty_program=False,
        )

        return [daimler_dealer, volvo_dealer, paccar_dealer]

    def run(self) -> SimulationResult:
        manufacturers = self._build_manufacturers()
        dealerships = self._build_dealerships(manufacturers)
        market = Market(self.parameters, seed=self.seed)
        sales_history = market.simulate(self.months, dealerships)
        return SimulationResult(months=self.months, sales_history=sales_history)

