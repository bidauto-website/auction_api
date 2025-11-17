from pydantic import Field, BaseModel

from auction_api.types.common import DefinedSiteEnum


class VinOrLotIn(BaseModel):
    site: DefinedSiteEnum | None = Field(None, description="Auction of vehicle")
    vin_or_lot: str

    @classmethod
    def validate_site(cls, v):
        return v


