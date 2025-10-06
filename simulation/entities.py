"""Entity definitions for the truck dealership competition simulation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TruckModel:
    """Represents a truck model offered by a manufacturer."""

    name: str
    segment: str
    base_price: float
    fuel_efficiency: float
    tech_rating: float
    durability: float

    def desirability(self, weightings: Dict[str, float]) -> float:
        """Compute a desirability score using weighted attributes."""
        return (
            weightings.get("price", 0.0) * (1 / self.base_price)
            + weightings.get("fuel_efficiency", 0.0) * self.fuel_efficiency
            + weightings.get("tech_rating", 0.0) * self.tech_rating
            + weightings.get("durability", 0.0) * self.durability
        )


@dataclass
class Manufacturer:
    """Represents a truck manufacturer."""

    name: str
    reputation: float
    innovation: float
    service_network: float
    marketing_power: float
    models: List[TruckModel] = field(default_factory=list)

    def overall_strength(self) -> float:
        """Weighted strength used for baseline demand splitting."""
        return (
            self.reputation * 0.3
            + self.innovation * 0.25
            + self.service_network * 0.25
            + self.marketing_power * 0.2
        )


@dataclass
class Dealership:
    """Represents a dealership competing in the market."""

    name: str
    manufacturer: Manufacturer
    local_relationships: float
    salesforce: float
    inventory: Dict[str, int]
    price_adjustment: float = 0.0
    marketing_spend: float = 0.0
    service_quality: float = 0.5
    loyalty_program: bool = False

    def effective_price(self, model: TruckModel) -> float:
        """Compute effective price after adjustments."""
        return model.base_price * (1 + self.price_adjustment)

    def sales_capacity(self) -> float:
        """Simplified measure of how many trucks the dealership can sell."""
        return self.salesforce * (1 + self.marketing_spend)

    def customer_experience(self) -> float:
        """Score capturing overall dealership experience."""
        loyalty_bonus = 0.1 if self.loyalty_program else 0.0
        return self.local_relationships * 0.4 + self.service_quality * 0.4 + loyalty_bonus

    def select_model_for_sale(self, segment: str) -> TruckModel | None:
        """Pick the most desirable model in stock for a given segment."""
        candidates = [m for m in self.manufacturer.models if m.segment == segment]
        candidates = [m for m in candidates if self.inventory.get(m.name, 0) > 0]
        if not candidates:
            return None
        return max(candidates, key=lambda m: m.tech_rating + m.durability)

    def record_sale(self, model_name: str) -> None:
        """Reduce inventory when a sale is made."""
        if model_name in self.inventory:
            self.inventory[model_name] -= 1

