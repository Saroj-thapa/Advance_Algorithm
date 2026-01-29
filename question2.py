"""
In this problem, we are given a row of tiles, where each tile has a score multiplier.
The goal is to shatter all the tiles one by one.
When a tile is shattered, the points gained are calculated using the tile itself and its immediate left and right tiles.
If a tile is at the start or end, the missing neighbor is treated as having a value of 1.
The total score depends on the order in which the tiles are shattered.
Our task is to find the order of shattering tiles that gives the maximum total points.
"""

"""This problem is solved using Dynamic Programming.
Instead of trying all possible orders, we break the problem into smaller parts.
We assume that the last tile to be shattered in a given range is known.
When the last tile is chosen, the problem splits into two smaller independent parts on the left and right.
We store the best score for each range of tiles in a table.
We solve the problem for small ranges first and then build up to larger ranges.
By checking all possible last tiles for every range, we ensure the maximum score is found.
Finally, the value stored for the full range gives the maximum total points.
"""

"""Dynamic Programming is used because this problem has many overlapping subproblems.
The total score depends on the order in which tiles are shattered.
Trying all possible orders would take too much time.
When one tile is shattered last, the tiles on the left and right become independent smaller problems.
The same tile ranges are solved again and again if we use a normal recursive approach.
Dynamic Programming stores the best result for each tile range so it is not recalculated.
This makes the solution efficient and faster.
Dynamic Programming also guarantees that the maximum total score is found.
"""
def max_points(tile_multipliers):
    # Step 1: Add 1 at the beginning and end
    # This handles the rule that out-of-bounds tiles are treated as 1
    a = [1] + tile_multipliers + [1]
    n = len(a)

    # Step 2: Create a DP table filled with zeros
    # dp[l][r] will store the maximum points
    # we can get by shattering tiles between index l and r
    dp = []
    for _ in range(n):
        dp.append([0] * n)

    # Step 3: Solve the problem for increasing interval sizes
    # length represents the distance between l and r
    for length in range(2, n):
        # l is the left boundary of the interval
        for l in range(0, n - length):
            # r is the right boundary of the interval
            r = l + length

            best = 0  # store the best score for this interval

            # Try each tile k as the last one to be shattered
            for k in range(l + 1, r):
                # Points gained by shattering tile k last
                # = points from left part + right part + current shatter score
                score = dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]

                # Keep the maximum score
                if score > best:
                    best = score

            # Store the best score for interval (l, r)
            dp[l][r] = best

    # Step 4: The answer for the full range of tiles
    return dp[0][n - 1]


# Test cases from the assignment
print(max_points([3, 1, 5, 8]))  
print(max_points([1, 5])) 
"""output167
10"""
