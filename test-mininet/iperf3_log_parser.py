#!/usr/bin/env python

import re

# Extract time and bandwidth from log
REGEX = r'(\d+\.\d+)-\d+\.\d+ +sec +\d+\.*\d* \w+ +(\d+\.*\d*) (\w+)/sec'

def main():
    regex = re.compile(REGEX)
    last_t = -1

    while True:
        try:
            line = input()
        except:
            # EOF
            break

        result = regex.search(line)
        if result is not None:
            t = float(result[1])
            bw = float(result[2])
            unit = result[3]

            # Regularize to Mbps
            if unit == 'Kbits':
                bw /= 1000
            elif unit == 'bits':
                bw /= 1000000

            if t <= last_t:
                # Average
                break
            last_t = t

            print(f'{t} {bw}')

if __name__ == '__main__':
    main()
