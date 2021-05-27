#!/usr/bin/env python

import re

# Extract time and cwnd from log
REGEX = r'(\d+\.\d+)-\d+\.\d+ +sec +\d+\.*\d* \w+ +\d+\.*\d* \w+/sec +\d+ +(\d+\.*\d*) (\w+)'

def main():
    regex = re.compile(REGEX)

    while True:
        try:
            line = input()
        except:
            # EOF
            break

        result = regex.search(line)
        if result is not None:
            t = float(result[1])
            cwnd = float(result[2])
            unit = result[3]

            # Regularize to Bytes
            if unit == 'MBytes':
                cwnd *= 1000000
            elif unit == 'KBytes':
                cwnd *= 1000
            
            # Assuming packet lengths are 1500 Bytes (1 MTU)
            cwnd /= 1500

            print(f'{t} {cwnd}')

if __name__ == '__main__':
    main()
