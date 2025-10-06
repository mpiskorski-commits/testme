"""Market simulation logic for competing truck dealerships."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .entities import Dealership, Manufacturer, TruckModel


@dataclass
class MarketParameters:
    """Parameters controlling market behavior."""

    base_demand: int = 120
    economic_volatility: float = 0.15
    fleet_growth_rate: float = 0.02
    price_sensitivity: float = 0.4
    experience_weight: float = 0.3
    technology_weight: float = 0.2
    fuel_weight: float = 0.1
    durability_weight: float = 0.2
    reputation_weight: float = 0.2


class Market:
    """Simulates demand allocation between dealerships."""

    def __init__(self, parameters: MarketParameters | None = None, seed: int | None = None) -> None:
        self.parameters = parameters or MarketParameters()
        self.random = random.Random(seed)
        self.history: List[Dict[str, float]] = []

    def _effective_demand(self, month: int) -> float:
        seasonal = 1 + 0.1 * math.sin(month * math.pi / 6)
        economic_noise = self.random.uniform(-self.parameters.economic_volatility, self.parameters.economic_volatility)
        trend = (1 + self.parameters.fleet_growth_rate) ** month
        return max(0.0, self.parameters.base_demand * seasonal * (1 + economic_noise) * trend)

    def _baseline_share(self, dealers: Iterable[Dealership]) -> Dict[str, float]:
        strengths = {d.name: d.manufacturer.overall_strength() for d in dealers}
        total = sum(strengths.values()) or 1.0
        return {name: strength / total for name, strength in strengths.items()}

    def _segment_preferences(self, model: TruckModel) -> float:
        weights = {
            "price": self.parameters.price_sensitivity,
            "fuel_efficiency": self.parameters.fuel_weight,
            "tech_rating": self.parameters.technology_weight,
            "durability": self.parameters.durability_weight,
        }
        return model.desirability(weights)

    def _dealer_competitiveness(self, dealer: Dealership, model: TruckModel) -> float:
        price_factor = 1 / dealer.effective_price(model)
        experience_factor = dealer.customer_experience() * self.parameters.experience_weight
        capacity_factor = dealer.sales_capacity() ** 0.5
        reputation_factor = dealer.manufacturer.reputation * self.parameters.reputation_weight
        product_factor = self._segment_preferences(model)
        return price_factor + experience_factor + capacity_factor + reputation_factor + product_factor

    def simulate_month(self, month: int, dealers: List[Dealership]) -> Dict[str, float]:
        demand = self._effective_demand(month)
        baseline = self._baseline_share(dealers)
        allocations: Dict[str, float] = {d.name: 0.0 for d in dealers}
        product_choices: Dict[Tuple[str, str], int] = {}

        for dealer in dealers:
            baseline_demand = demand * baseline[dealer.name]
            available_segments = {model.segment for model in dealer.manufacturer.models}
            for segment in available_segments:
                model = dealer.select_model_for_sale(segment)
                if model is None:
                    continue
                competitiveness = self._dealer_competitiveness(dealer, model)
                product_choices[(dealer.name, model.name)] = competitiveness

            competitiveness_total = sum(
                competitiveness
                for (dealer_name, _), competitiveness in product_choices.items()
                if dealer_name == dealer.name
            )
            if competitiveness_total == 0:
                continue
            for (dealer_name, model_name), competitiveness in list(product_choices.items()):
                if dealer_name != dealer.name:
                    continue
                share = competitiveness / competitiveness_total
                sales = baseline_demand * share
                dealer.record_sale(model_name)
                allocations[dealer.name] += sales

        self.history.append(allocations)
        return allocations

    def simulate(self, months: int, dealers: List[Dealership]) -> List[Dict[str, float]]:
        """Run the simulation across multiple months."""
        results = []
        for month in range(months):
            results.append(self.simulate_month(month, dealers))
        return results

