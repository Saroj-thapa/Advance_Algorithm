"""This problem deals with optimizing electricity distribution in a smart energy grid that supplies power 
to three districts, namely A, B, and C. Each district has a different electricity demand at every hour of the day,
and this demand must be satisfied within an allowable tolerance of ±10%. 
The electricity is generated from multiple sources such as solar, hydro, and diesel, 
where each source has specific operating hours, maximum generation capacity, and cost per unit of energy. 
The main objective is to minimize the overall cost of electricity production while ensuring reliable power supply
to all districts. Renewable energy sources like solar and hydro are preferred due to their lower cost and 
environmental benefits, whereas diesel power is considered a backup option and is used only when renewable 
sources cannot meet the demand. The problem requires making smart hour-by-hour decisions that balance cost, 
availability, capacity constraints, and sustainability."""

"""We solve this problem in a step-by-step, practical way (like how a real grid operator would do it). 
For each hour, we first read the electricity demand of District A, B, and C. 
Then we check which energy sources are available at that hour (for example, solar works only in daytime, 
diesel only in evening, hydro may work most of the day) and note how much capacity each source can provide. 
After that, we allocate electricity by priority: we use the cheapest and renewable sources first 
(usually Solar → Hydro → Diesel) to keep the cost low and maximize clean energy. 
We distribute the available energy to districts that still need power until either the district demand is met 
or the source capacity finishes. If solar and hydro are not enough, we use diesel as a backup to fill the 
remaining demand. Once allocation is done, we check the ±10% rule to confirm that each district received 
electricity within the allowed range (not too little and not too much). Finally, we calculate 
the cost for that hour by multiplying the energy taken from each source by its cost, and we 
repeat the same process for all hours. At the end, we add up the total cost, compute the total 
percentage of renewable energy used, and report when and why diesel was needed.
"""

#  SMART ENERGY GRID (Simple) 
# This solution uses a simple greedy method:
# 1) Use renewable + cheaper sources first (Solar -> Hydro -> Diesel)
# 2) Try to meet each district's demand (exactly if possible)
# 3) Check if supply is within ±10% of demand

from dataclasses import dataclass

@dataclass
class Source:
    name: str
    capacity_per_hour: float
    start_hour: int     # source available from this hour (inclusive)
    end_hour: int       # source available until this hour (inclusive)
    cost_per_kwh: float
    renewable: bool

def is_available(source, hour):
    """This checks if a source can be used at this hour."""
    return source.start_hour <= hour <= source.end_hour

def allocate_one_hour(hour, demand, sources):
    """
    Allocate energy for one hour.

    demand is like: {"A": 20, "B": 15, "C": 25}

    Returns:
    allocation: {"A": {"Solar":x,"Hydro":y,"Diesel":z}, ...}
    fulfilled: {"A": supplied, "B": supplied, "C": supplied}
    hour_cost: total money cost for this hour
    """

    # Create empty allocation table for each district and each source
    allocation = {d: {s.name: 0.0 for s in sources} for d in demand}

    # Keep track of how much each district still needs
    remaining_need = {d: float(demand[d]) for d in demand}

    # For this hour, calculate how much capacity each source has
    cap_left = {}
    for s in sources:
        cap_left[s.name] = s.capacity_per_hour if is_available(s, hour) else 0.0

    # Sort sources by cost (cheapest first)
    sources_sorted = sorted(sources, key=lambda x: x.cost_per_kwh)

    # Greedy filling: give energy from cheapest source first
    for s in sources_sorted:
        available_energy = cap_left[s.name]

        # If this source has no capacity at this hour, skip
        if available_energy <= 0:
            continue

        # Give energy to districts that still need energy
        for d in demand:
            if available_energy <= 0:
                break

            need = remaining_need[d]

            # If this district already got full demand, skip
            if need <= 0:
                continue

            # Give as much as possible (but not more than needed)
            give = min(need, available_energy)

            allocation[d][s.name] += give
            remaining_need[d] -= give
            available_energy -= give

        # Update remaining capacity of this source
        cap_left[s.name] = available_energy

    # Calculate how much each district received
    fulfilled = {d: sum(allocation[d].values()) for d in demand}

    # Calculate total cost for this hour
    hour_cost = 0.0
    for d in allocation:
        for s in sources:
            hour_cost += allocation[d][s.name] * s.cost_per_kwh

    return allocation, fulfilled, hour_cost

def within_tolerance(demand, fulfilled, tol=0.10):
    """
    Checks if each district got supply within ±10% of demand.
    """
    for d in demand:
        low = demand[d] * (1 - tol)
        high = demand[d] * (1 + tol)

        if not (low <= fulfilled[d] <= high):
            return False
    return True

# user name 
if __name__ == "__main__":

    print("SMART ENERGY GRID OPTIMIZATION  ")

    # ---- Sources (You can keep these as assignment defaults) ----
    # Change these numbers if your PDF has different values
    sources = [
        Source("Solar", 50, 6, 18, 1.0, True),   # Example: solar works 6 to 18
        Source("Hydro", 40, 0, 23, 1.5, True),   # Example: hydro works all day
        Source("Diesel", 60, 17, 23, 3.0, False) # Example: diesel works 17 to 23
    ]

    # Ask user for how many hours they want to enter
    H = int(input("\nEnter number of hours to simulate (example 24): "))

    # Take demand for each hour from user
    # demand_table[hour] = {"A":..., "B":..., "C":...}
    demand_table = {}

    print("\nEnter demands for each hour (District A, B, C):")
    for _ in range(H):
        hour = int(input("\nHour (0-23): "))
        a = float(input("  Demand for District A: "))
        b = float(input("  Demand for District B: "))
        c = float(input("  Demand for District C: "))
        demand_table[hour] = {"A": a, "B": b, "C": c}

    #  Run simulation 
    total_cost = 0.0
    total_energy = 0.0
    renewable_energy = 0.0
    diesel_used_log = []

    tolerance = 0.10  # ±10% rule

    for hour in sorted(demand_table.keys()):
        demand = demand_table[hour]

        allocation, fulfilled, hour_cost = allocate_one_hour(hour, demand, sources)
        ok = within_tolerance(demand, fulfilled, tol=tolerance)

        print(f"\n========== Hour {hour:02d} ==========")
        print("Feasible within ±10% ?", ok)
        print("District | Demand | Solar | Hydro | Diesel | Supplied")

        for d in ["A", "B", "C"]:
            solar = allocation[d]["Solar"]
            hydro = allocation[d]["Hydro"]
            diesel = allocation[d]["Diesel"]
            supplied = fulfilled[d]

            print(f"{d:8} | {demand[d]:6.1f} | {solar:5.1f} | {hydro:5.1f} | {diesel:6.1f} | {supplied:7.1f}")

            # Keep diesel usage log for reporting
            if diesel > 0:
                diesel_used_log.append((hour, d, diesel))

            # Count renewable energy used
            renewable_energy += solar + hydro
            total_energy += supplied

        print(f"Hour Cost: Rs. {hour_cost:.2f}")
        total_cost += hour_cost

    #  Final summary
    renewable_percent = (renewable_energy / total_energy) * 100 if total_energy > 0 else 0

    print("\n================ FINAL SUMMARY ================")
    print(f"Total Cost: Rs. {total_cost:.2f}")
    print(f"Renewable Percentage Used: {renewable_percent:.2f}%")

    if diesel_used_log:
        print("\nDiesel was used at these times (because solar/hydro were not enough or solar unavailable):")
        for hour, district, amount in diesel_used_log:
            print(f"  Hour {hour:02d}, District {district} -> Diesel {amount:.1f} kWh")
    else:
        print("\nDiesel was NOT used.")

"""output
Enter number of hours to simulate (example 24): 2

Enter demands for each hour (District A, B, C):

Hour (0-23): 22
  Demand for District A: 10
  Demand for District B: 8
  Demand for District C: 2

Hour (0-23): 22
  Demand for District A: 3
  Demand for District B: 8
  Demand for District C: 13

========== Hour 22 ==========
Feasible within ±10% ? True
District | Demand | Solar | Hydro | Diesel | Supplied
A        |    3.0 |   0.0 |   3.0 |    0.0 |     3.0
B        |    8.0 |   0.0 |   8.0 |    0.0 |     8.0
C        |   13.0 |   0.0 |  13.0 |    0.0 |    13.0
Hour Cost: Rs. 36.00

================ FINAL SUMMARY ================
Total Cost: Rs. 36.00
Renewable Percentage Used: 100.00%

Diesel was NOT used."""