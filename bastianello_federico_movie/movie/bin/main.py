

import converter
import sys
import os


if __name__ == "__main__":
    result = converter.main(len(sys.argv), sys.argv, [(key,value) for key, value in os.environ.items()])
    print("stato di uscita dal programma: ", result)
    sys.exit(result)

