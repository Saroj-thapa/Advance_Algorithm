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

# SHORT VERSION - Smart Energy Grid Optimization

# Hourly demand of each district in kWh.
# This shows how much energy each district needs at a particular hour.
demand = {
    6: {"A": 20, "B": 15, "C": 25},
    7: {"A": 22, "B": 16, "C": 28},
}

# Information about energy sources.
# capacity means maximum energy the source can supply per hour.
# cost means cost per unit (kWh).
# availability means the hours during which the source can be used.
sources = {
    "Solar": {
        "capacity": 50,
        "cost": 1.0,
        "availability": range(6, 19)   # Solar works from 6 AM to 6 PM
    },
    "Hydro": {
        "capacity": 40,
        "cost": 1.5,
        "availability": range(0, 24)   # Hydro works all day
    },
    "Diesel": {
        "capacity": 60,
        "cost": 3.0,
        "availability": range(17, 24)  # Diesel works in the evening and night
    }
}

# These values represent the ±10% tolerance rule.
# Each district must receive at least 90% and at most 110% of its demand.
TOL_LOW = 0.90
TOL_HIGH = 1.10


def allocate_energy(hour, hour_demand):
    """
    This function allocates energy for one hour.

    First, it selects the energy sources that are available at that hour.
    Then, it uses a greedy approach by choosing the cheapest source first.
    Energy is supplied to districts until either demand or capacity is finished.
    """

    allocation = {}                # Stores how much energy each source gives to each district
    remaining = hour_demand.copy() # Keeps track of remaining unmet demand
    total_cost = 0.0               # Total cost for this hour

    # Select only sources that can operate during this hour
    available_sources = {
        s: data for s, data in sources.items()
        if hour in data["availability"]
    }

    # Sort the available sources by cost so cheaper sources are used first
    sorted_sources = sorted(
        available_sources.items(),
        key=lambda x: x[1]["cost"]
    )

    # Allocate energy from each source
    for source, data in sorted_sources:
        allocation[source] = {}
        capacity_left = data["capacity"]

        # Try to satisfy the demand of each district
        for district in remaining:
            if remaining[district] <= 0 or capacity_left <= 0:
                continue

            # Give the minimum of remaining demand or available capacity
            energy_given = min(remaining[district], capacity_left)

            allocation[source][district] = energy_given
            remaining[district] -= energy_given
            capacity_left -= energy_given
            total_cost += energy_given * data["cost"]

    return allocation, remaining, total_cost


def demand_satisfied(original, supplied):
    """
    This function checks whether each district
    received energy within the allowed ±10% range.
    """
    for district in original:
        lower = TOL_LOW * original[district]
        upper = TOL_HIGH * original[district]

        if not (lower <= supplied[district] <= upper):
            return False
    return True


total_cost_all = 0.0
total_energy_all = 0.0
renewable_all = 0.0
diesel_usage = []

print("\nENERGY ALLOCATION TABLE")
print("-" * 90)
print("Hour | District | Solar | Hydro | Diesel | Total Used | Demand | % Met")
print("-" * 90)

# Run the energy allocation for each hour
for hour, hour_demand in demand.items():
    allocation, remaining, cost = allocate_energy(hour, hour_demand)
    total_cost_all += cost

    # Calculate total energy supplied to each district from all sources
    supplied = {d: 0.0 for d in hour_demand}

    for source in allocation:
        for district, energy in allocation[source].items():
            supplied[district] += energy

            # Track totals for final report
            total_energy_all += energy
            if source in ("Solar", "Hydro"):
                renewable_all += energy
            if source == "Diesel" and energy > 0:
                diesel_usage.append((hour, district))

    # Check if demand is satisfied within ±10%
    if not demand_satisfied(hour_demand, supplied):
        print(f"Warning: Hour {hour} demand not satisfied within ±10%")

    # Print results for each district
    for district in hour_demand:
        solar = allocation.get("Solar", {}).get(district, 0.0)
        hydro = allocation.get("Hydro", {}).get(district, 0.0)
        diesel = allocation.get("Diesel", {}).get(district, 0.0)

        total_used = solar + hydro + diesel
        demand_val = hour_demand[district]
        fulfilled = (total_used / demand_val) * 100 if demand_val > 0 else 0

        print(f"{hour:>4} | {district:>8} | {solar:>5.0f} | {hydro:>5.0f} | {diesel:>6.0f} |"
              f" {total_used:>10.0f} | {demand_val:>6.0f} | {fulfilled:>5.1f}%")


print("\nANALYSIS REPORT")
print("-" * 40)
print(f"Total Cost of Distribution: Rs. {total_cost_all:.2f}")

renewable_percentage = (renewable_all / total_energy_all) * 100 if total_energy_all > 0 else 0
print(f"Renewable Energy Usage: {renewable_percentage:.2f}%")

if diesel_usage:
    print("Diesel used in:")
    for h, d in diesel_usage:
        print(f"  Hour {h}, District {d} (diesel used because renewable energy was insufficient)")
else:
    print("Diesel was not used in the provided hours.")

"""------------------------------------------------------------------------------------------
Hour | District | Solar | Hydro | Diesel | Total Used | Demand | % Met
------------------------------------------------------------------------------------------
   6 |        A |    50 |     0 |      0 |         50 |     50 | 100.0%
   6 |        B |     0 |    10 |      0 |         10 |     10 | 100.0%
   6 |        C |     0 |     0 |      0 |          0 |      0 |   0.0%

ANALYSIS REPORT
----------------------------------------
Total Cost of Distribution: Rs. 65.00
Renewable Energy Usage: 100.00%
Diesel was not used in the provided hours."""