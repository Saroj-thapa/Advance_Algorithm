""" In this problem, a salesman must visit all given cities exactly once and then return to the starting city. 
Each city has a position on a 2D plane, and the distance between cities is calculated using Euclidean distance.
The goal of the problem is to find a route (tour) that visits every city and 
has the minimum possible total travel distance.
However, as the number of cities increases, checking all possible routes becomes computationally 
impossible because the number of routes grows very fast. 
Therefore, an exact solution is not practical for large inputs.
"""

"""Since finding the perfect solution is difficult, the problem is solved using Simulated Annealing, 
which is a heuristic (approximation) algorithm.
Simulated Annealing is inspired by the process of cooling hot metal. 
When metal is hot, atoms move freely. As it cools down slowly, atoms settle into a stable structure. 
In the same way, this algorithm starts with a high level of randomness and gradually 
reduces it to reach a good solution.
This approach helps avoid getting stuck in a local minimum
(a solution that looks good but is not the best overall).
"""

"""This problem is solved using the simulated annealing algorithm, which is an approximation method used for 
difficult optimization problems like the Traveling Salesperson Problem. 
First, a set of cities is generated with random coordinates, and an initial tour is created by visiting all cities 
in a random order. The total distance of this tour is calculated using the Euclidean distance between cities, 
including the return to the starting city. Then, a new tour is created by making small changes to the current tour,
such as swapping two cities or reversing a section of the tour using the 2-opt method. 
If the new tour has a shorter distance, it is accepted immediately; if it is longer,
 it may still be accepted with a certain probability depending on the current temperature. 
 This acceptance of worse solutions helps the algorithm avoid getting stuck in poor local solutions. 
 After each iteration, the temperature is gradually reduced using either exponential or linear cooling. 
This process is repeated many times until the temperature becomes very low or the maximum number of iterations is reached, and finally, 
the shortest tour found during the entire process is returned as the solution.
"""
import random
import math

# Calculate distance between two cities
def distance(city1, city2):
    """Calculate straight-line distance between two points"""
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Calculate total distance of a tour
def tour_distance(tour, cities):
    """Add up all distances in the tour"""
    total = 0
    
    # Distance between each pair of consecutive cities
    for i in range(len(tour)):
        current_city = cities[tour[i]]
        next_city = cities[tour[(i + 1) % len(tour)]]  # % wraps back to start
        total += distance(current_city, next_city)
    
    return total

# Swap two cities in the tour (creates a neighbor)
def swap_cities(tour):
    """Swap two random cities to create a new tour"""
    new_tour = tour.copy()
    i = random.randint(0, len(tour) - 1)
    j = random.randint(0, len(tour) - 1)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

# Simulated Annealing Algorithm
def simulated_annealing(cities, cooling_type='exponential'):
    """
    Find a good tour using simulated annealing
    cooling_type: 'exponential' or 'linear'
    """
    
    # Step 1: Start with a random tour
    n = len(cities)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_distance = tour_distance(current_tour, cities)
    
    # Keep track of best solution
    best_tour = current_tour.copy()
    best_distance = current_distance
    
    # Step 2: Set initial temperature (high to allow exploration)
    temperature = 10000
    
    # Step 3: Main loop
    for iteration in range(5000):

        # Create a neighboring solution by swapping two cities
        new_tour = swap_cities(current_tour)
        new_distance = tour_distance(new_tour, cities)
        
        # Calculate how much worse the new solution is
        difference = new_distance - current_distance
        
        # Decide: should we accept this new solution?
        if difference < 0:
            # New solution is better - always accept
            current_tour = new_tour
            current_distance = new_distance
            
            # Update best if this is the best we've seen
            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance
        else:
            # New solution is worse - maybe accept it anyway
            # This helps us escape getting stuck
            probability = math.exp(-difference / temperature)
            if random.random() < probability:
                current_tour = new_tour
                current_distance = new_distance
        
        # Step 4: Cool down temperature
        if cooling_type == 'exponential':
            temperature = temperature * 0.995  # Multiply by 0.995
        else:
            temperature = temperature - 2  # Subtract 2
        
        # Stop if too cold
        if temperature < 1:
            break
    
    return best_tour, best_distance

# Main program
if __name__ == "__main__":
    
    # Generate 20 random cities
    cities = []
    for i in range(20):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        cities.append((x, y))
    
    print(f"Created {len(cities)} cities")
    print(f"First 3 cities: {cities[:3]}\n")
    
    # Test 1: Exponential cooling
    print("=== Test 1: Exponential Cooling ===")
    tour1, dist1 = simulated_annealing(cities, 'exponential')
    print(f"Best distance found: {dist1:.2f}")
    print(f"Tour order: {tour1}\n")
    
    # Test 2: Linear cooling
    print("=== Test 2: Linear Cooling ===")
    tour2, dist2 = simulated_annealing(cities, 'linear')
    print(f"Best distance found: {dist2:.2f}")
    print(f"Tour order: {tour2}\n")
    
    # Compare
    print("=== Comparison ===")
    if dist1 < dist2:
        print(f"Exponential is better: {dist1:.2f} < {dist2:.2f}")
    else:
        print(f"Linear is better: {dist2:.2f} < {dist1:.2f}")
"""Created 20 cities
First 3 cities: [(934.6841528376591, 982.2702676523938), (719.940406016339, 780.8666712880505), 
(979.4673858738323, 476.9913838804449)]

=== Test 1: Exponential Cooling ===
Best distance found: 4626.94
Tour order: [15, 4, 1, 0, 11, 19, 18, 16, 13, 8, 2, 12, 5, 10, 6, 17, 14, 3, 7, 9]

=== Test 2: Linear Cooling ===
Best distance found: 6132.48
Tour order: [1, 10, 2, 12, 5, 13, 18, 19, 11, 6, 14, 17, 15, 4, 16, 0, 8, 9, 7, 3]

=== Comparison ===
Exponential is better: 4626.94 < 6132.48"""