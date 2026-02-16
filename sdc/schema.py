from pydantic import BaseModel
from typing import Literal

Path = Literal["A_REPAY", "B_RESTRUCTURE"]
Timing = Literal["IMMEDIATE", "GRADUAL", "DELAYED"]
Perimeter = Literal["EXTERNAL_ONLY", "EXTERNAL_PLUS_CFA_PARTIAL"]
FiscalIntensity = Literal["MODERATE", "HIGH", "EXTREME"]
FinancingMix = Literal["UEMOA_HEAVY", "CONCESSIONAL_HEAVY", "HIGH_INTEREST"]
SocialPriority = Literal["PROTECT", "NEUTRAL", "COMPRESS"]

class Scenario(BaseModel):
    name: str = "Untitled scenario"
    path: Path = "A_REPAY"
    timing: Timing = "IMMEDIATE"
    perimeter: Perimeter = "EXTERNAL_ONLY"
    fiscal_intensity: FiscalIntensity = "HIGH"
    financing_mix: FinancingMix = "CONCESSIONAL_HEAVY"
    social_priority: SocialPriority = "NEUTRAL"
