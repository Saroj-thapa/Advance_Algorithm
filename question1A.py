import math
"""In this problem, we are given the locations of several sensors on a 2D plane.
Each sensor has fixed coordinates (x, y).
We need to place one central data hub at the best possible location.
The aim is to reduce signal loss, which increases with distance.
So, the hub should be placed such that the total distance from the hub to all sensors is minimum.
The distance used is the straight-line (Euclidean) distance.
The final result should be the minimum possible sum of these distances.
"""
""" We solve this problem using the geometric median.
The geometric median is the point that gives the smallest total distance to all sensors.
First, we check if there are no sensors.
If there are no sensors, the total distance is zero.
Next, we place the hub at the average position of all sensors.
This gives us a good starting point.
Then, we calculate the distance from the hub to each sensor.
We use the Euclidean distance formula for this.
Sensors that are closer should affect the hub position more.
So, we give more weight to closer sensors.
Using these weights, we calculate a new position for the hub.
This moves the hub closer to the best location.
We repeat this process many times.
Each time, the hub moves a little closer to the geometric median.
When the hub position changes very little, we stop.
This means we have found the best position.
Finally, we calculate the total distance from the hub to all sensors.
This is the minimum total distance.
"""

def total_distance(x, y, sensors):
    """
    This function calculates how far the hub is
    from all sensors combined.
    """
    total = 0

    # Go through each sensor one by one
    for sx, sy in sensors:
        # Use distance formula to find distance
        # between hub (x, y) and sensor (sx, sy)
        distance = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)

        # Add this distance to total
        total += distance

    # Return the final total distance
    return total

def min_total_distance(sensors):
    """
    This function finds the best location to place the hub
    so that the total distance to all sensors is minimum.
    """

    # If there are no sensors, distance is zero
    if len(sensors) == 0:
        return 0.0

    #  STEP 1: Start from the center 
    # We begin from the average position of all sensors
    x = 0
    y = 0

    # Add all sensor coordinates
    for sx, sy in sensors:
        x += sx
        y += sy

    # Divide by number of sensors to get average
    x = x / len(sensors)
    y = y / len(sensors)

    #  STEP 2: Improve the hub position 
    # Repeat the process many times to get closer
    for _ in range(1000):

        # These variables help calculate new position
        num_x = 0
        num_y = 0
        den = 0

        # Check distance from current hub to each sensor
        for sx, sy in sensors:
            distance = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)

            # If hub is exactly on a sensor,
            # we already found the best place
            if distance == 0:
                return total_distance(x, y, sensors)

            # Closer sensors get more importance (weight)
            weight = 1 / distance

            # Weighted sum of x and y coordinates
            num_x += weight * sx
            num_y += weight * sy
            den += weight

        # Calculate new hub position
        new_x = num_x / den
        new_y = num_y / den

        # If the hub position changes very little,
        # we stop because we are close enough
        if math.sqrt((new_x - x) ** 2 + (new_y - y) ** 2) < 0.000001:
            x = new_x
            y = new_y
            break

        # Update hub position and repeat
        x = new_x
        y = new_y

    # STEP 3: Calculate final answer
    return total_distance(x, y, sensors)


# user input section

# Ask user how many sensors are there
n = int(input("Enter number of sensors: "))

sensors = []

# Take coordinates of each sensor
for i in range(n):
    print(f"Enter coordinates of sensor {i + 1}:")
    x = float(input("  x: "))
    y = float(input("  y: "))

    # Store sensor position in list
    sensors.append([x, y])

# Find the minimum total distance
answer = min_total_distance(sensors)

# Show the final result
print("\nMinimum total distance from hub to all sensors:")
print(round(answer, 5))
"""output 
PS C:\Users\krita\OneDrive\Desktop\Advance Algorithm> & C:\Users\krita\AppData\Local\Programs\Python\Python313\python.exe "c:/Users/krita/OneDrive/Desktop/Advance Algorithm/question1A.py"
Enter number of sensors: 2
Enter coordinates of sensor 1:
  x: 1
  y: 1
Enter coordinates of sensor 2:
  x: 3
  y: 3

Minimum total distance from hub to all sensors:
2.82843
"""