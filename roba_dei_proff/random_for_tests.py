import random
import time


def make_test(lab, n, base, spread, random_file):
    """
        Writes a test description with the label `lab` to the file.
        Generates a sequence of `n` elements starting at `base`.
        The average distance between elements is uniformly distributed in [0, spread].
    """
    elem = base
    v = []
    
    random_file.write(f"{lab} ")
    
    for _ in range(n): 
        # Make elements
        elem += random.randint(0, spread) 
        v.append(elem)
    
    val = base + random.randint(0, elem - base)  # Make search value
    random_file.write(f"{val} {{ ")
    found = 0
    
    for item in v:
        # Print elements and check if val is found
        if item == val:
            found = 1
        random_file.write(f"{item} ")
    
    random_file.write(f" }} {found} \n")


def main():
    start = time.process_time_ns()      
    print("At the beginning of the process") 
    print("Process Time (in nanoseconds):", start, "\n") 
    
    # Open the output file
    with open("my_tests.txt", "w", encoding="utf-8") as random_file:
        # Generate about 50 tests
        no_of_tests = random.randint(0, 100)
        for i in range(no_of_tests):
            lab = ""
            make_test(
                lab + str(i + 1),
                random.randint(0, 500),     # Number of elements
                0,                          # Base
                random.randint(0, 50),      # Spread
                random_file
            )
    end = time.process_time_ns()     
    print("\nAt the end of the process") 
    print("Process time (in nanoseconds):", end)      
    print("Elapsed time during the process (in nanoseconds):", end - start)   


if __name__ == "__main__":
    main()
