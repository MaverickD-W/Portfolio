from pydantic import BaseModel, computed_field, ConfigDict
from typing import ClassVar
import acquire
import pprint
import pandas as pd


class SubwayLine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    route_name: str
    route_id: str
    df: pd.DataFrame

    @computed_field
    @property
    def stops(self) -> list[str]:
        """Ordered list of parent_station names along the line."""
        order = (
            self.df.groupby("parent_station")["stop_count"]
            .median()
            .sort_values()
        )
        return order.index.tolist()

    @computed_field
    @property
    def dates(self) -> list[str]:
        """Sorted list of service dates in February as strings."""
        return sorted(self.df["service_date"].astype(str).unique().tolist())

    @computed_field
    @property
    def daily_avg_travel(self) -> dict[str, float]:
        """Date string → mean actual travel time (seconds) across all trips."""
        # Sum travel_time_seconds per trip per day, then average across trips
        per_trip = (
            self.df
            .groupby(["service_date", "trip_id"])["travel_time_seconds"]
            .sum()
            .reset_index()
        )
        result = (
            per_trip
            .groupby("service_date")["travel_time_seconds"]
            .mean()
        )
        return {str(k): round(v, 2) for k, v in result.items()}

    @computed_field
    @property
    def daily_avg_scheduled(self) -> dict[str, float]:
        """Date string → mean scheduled travel time (seconds) across all trips."""
        per_trip = (
            self.df
            .groupby(["service_date", "trip_id"])["scheduled_travel_time"]
            .sum()
            .reset_index()
        )
        result = (
            per_trip
            .groupby("service_date")["scheduled_travel_time"]
            .mean()
        )
        return {str(k): round(v, 2) for k, v in result.items()}

    @computed_field
    @property
    def travel_by_stop_and_day(self) -> "pd.DataFrame":
        """
        Pivot table: rows = parent_station (in geographic order),
                     cols = service_date,
                     values = mean travel_time_seconds.
        This is the 2D array the heatmap animation calls set_array() on.
        """
        pivot = self.df.pivot_table(
            index="parent_station",
            columns="service_date",
            values="travel_time_seconds",
            aggfunc="mean",
        )
        # Reorder rows to match geographic stop order
        ordered_stops = [s for s in self.stops if s in pivot.index]
        pivot = pivot.loc[ordered_stops]
        pivot.columns = [str(c) for c in pivot.columns]
        return pivot


# --- Construction ---

sub_df = acquire.main()[0]

required_cols = ["trip_id", "stop_id", "stop_timestamp", "service_date",
                 "travel_time_seconds", "scheduled_travel_time",
                 "parent_station", "trunk_route_id"]

sub_df.sort_values(["service_date", "stop_timestamp"], inplace=True)
sub_df.drop_duplicates(subset=["stop_id", "trip_id"], inplace=True)
sub_df.dropna(subset=required_cols, inplace=True, ignore_index=True)


def make_line(sub_df: pd.DataFrame, route_id: str, route_name: str) -> SubwayLine:
    line_df = sub_df[sub_df["trunk_route_id"] == route_id].copy()
    return SubwayLine(route_name=route_name, route_id=route_id, df=line_df)

green_line = make_line(sub_df, route_id="Green", route_name="Green Line")


def main():
    print("=== STOPS ===")
    print(green_line.stops)
    
    print("\n=== DATES ===")
    print(green_line.dates)
    
    print("\n=== DAILY AVG ACTUAL TRAVEL (seconds) ===")
    for date, val in green_line.daily_avg_travel.items():
        print(f"  {date}: {val}")
    
    print("\n=== DAILY AVG SCHEDULED TRAVEL (seconds) ===")
    for date, val in green_line.daily_avg_scheduled.items():
        print(f"  {date}: {val}")
    
    print("\n=== TRAVEL BY STOP AND DAY (pivot table) ===")
    print(green_line.travel_by_stop_and_day.to_string())
    
    print("\n=== FULL MODEL DUMP ===")
    pprint.pprint(green_line.model_dump(exclude={"df", "travel_by_stop_and_day"}))
    
    green_line.travel_by_stop_and_day.to_csv("pivot.csv")

if __name__ == "__main__":
    main()
