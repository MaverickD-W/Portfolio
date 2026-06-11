from pydantic import BaseModel, Field, field_validator


class ParkConditions(BaseModel):

    UNIT_NAME: str
    date: str
    sensor_latitude: float = Field(le=-90, ge=90)
    sensor_longitude: float = Field(le=180, ge=-180)
    latitude: float = Field(le=-90, ge=90)
    longitude: float = Field(le=180, ge=-180)
    geometry: object
    so2: float | None
    pm25: float | None
    pm10: float | None
    co: float | None
    o3: float | None
    no2: float | None
    mean_temp: float
    max_temp: float
    temp_min: float
    wind_speed: float
    wind_gusts: float
    precipitation: float


    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        if value.split("-")[0] == "2025":
            return value
        elif value.split("-")[1] in [str(a) if a > 10 else ("0"+str(a)) for a in range(1,13)]:
            return value
        elif value.split("-")[2] in [str(a) if a > 10 else ("0"+str(a)) for a in range(1,32)]:
            return value
        else:
            raise ValueError(f"Invalid date format: {value}. Date should be from 2025-01-01 and 2025-12-31")

