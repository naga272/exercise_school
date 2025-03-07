
import binary_search
import re


def parse_string(s, pattern):
    # Define the regex pattern for matching the format: int int [ list_of_ints ] int
    match = re.match(pattern, s)    
    if match:
        # Extract each part of the match and convert appropriately
        first_int = int(match.group(1))
        second_int = int(match.group(2))
        list_of_ints = [int(num) for num in match.group(3).split()]
        fourth_int = int(match.group(4))        
        # Return the list in the desired format
        return [first_int, second_int, list_of_ints, fourth_int]
    else:
        raise ValueError("String format is incorrect")    


class Test:
    def __init__(self, label, val, seq, res):
        self.label = label
        self.val = val
        self.seq = seq
        self.res = res
        
    def __str__(self):
        return f'Test({self.label}, {self.val}, {self.seq}, {self.res} )'


def test_all():
    error_count = 0
    #for line in Lines:     
    # Strips the newline character
    for line in Lines:    
        line_to_string = line.strip('\n')        
        list_from_line = parse_string(line_to_string, r"(\d+)\s+(-?\d+)\s+\{\s*([0-9\s,]+)\s*\}\s+(\d+)")

        t = Test(list_from_line[0], list_from_line[1], list_from_line[2], list_from_line[3])
        r = binary_search.binary_search(t.seq, t.val)

        if (t.res != r):
            print(f"Failure: test {t.label}, {binary_search}: {len(t.seq)}, {elements}, val = {t.val}, -> {t.res}, ")
            error_count += 1

    return error_count


if __name__ == "__main__":
    file1 = open('my_tests.txt', 'r')
    Lines = file1.readlines()

    errors = test_all()

    print("Numbers of errors: ", errors)
    file1.close()
