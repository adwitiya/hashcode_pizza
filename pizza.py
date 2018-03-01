from __future__ import print_function
import sys
import numpy as np


def read_file(filename):
    '''Read File'''

    with open(filename, 'r') as f:
        line = f.readline()
        rows, cols, min_ingr, max_size = [int(n) for n in line.split()]

        pizza = np.zeros([rows, cols])
        for row in range(rows):
            for ing, col in zip(f.readline(), range(cols)):
                if ing == 'T':
                    pizza[row, col] = 1
                else:
                    pizza[row, col] = 0

    return pizza, min_ingr, max_size


def main():
    pizza, min_ingr, max_size = read_file('example.in')
    block = np.zeros_like(pizza).astype(int)
    output = []
    shapes = []
    for h in range(max_size, 0, -1):
        for w in range(max_size, 0, -1):
            if 2 * min_ingr <= h * w <= max_size:
                shapes.append((h, w))
    shapes.sort(key=lambda sort: (min(sort[0], sort[1]), max(sort[0], sort[1])), reverse=True)
    print('Shapes:', shapes, file=sys.stderr)  # print to stderr so we dont leak debug printing into output
    # print(pizza.shape[1])
    for d in range(pizza.shape[0] + pizza.shape[1] + 1):
        for i in range(d + 1):
            j = d - i
            if i >= pizza.shape[0] or j >= pizza.shape[1]:
                continue

            for h, w in shapes:
                if i + h > pizza.shape[0] or j + w > pizza.shape[1]:
                    continue
                if np.any(block[i:i + h, j:j + w]):  # already used in another slice
                    continue
                if not min_ingr <= np.sum(pizza[i:i + h, j:j + w]) <= h * w - min_ingr:  # not enough T or M
                    continue
                block[i:i + h, j:j + w] = 1
                output.append((i, j, i + h - 1, j + w - 1))
                break

    # print('Score:', np.sum(block), file=sys.stderr)
    with open('ex.out', 'w') as f:
        print(len(output))
        f.write('{}\n'.format(len(output)))
        for e in output:
            #print(e)
            string = ' '.join(map(str, e))
            f.write(string)
            f.write('\n')
        [print(' '.join(str(x) for x in e)) for e in output]


if __name__ == '__main__':
    main()
