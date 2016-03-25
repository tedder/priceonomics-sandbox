#!/usr/bin/env python3

import csv
import sys
import collections
import statistics

cityvals = collections.defaultdict(list)

# notes:
# - data seems to be really clean, actually. after normalizing the case of the city/state they came together.
# - how to represent large cities? (e.g., Manhattan vs New York City, Pasadena vs Los Angeles)
#   * leaving alone
#   * alternative: collect into census MSAs
# - some outliers with zero reviews- eg a $10000 tree fort in Park City. They could be excluded but where's the cutoff? Perhaps < 2 reviews?

c = 0
with open(sys.argv[1]) as csvfile:
  r = csv.DictReader(csvfile, fieldnames=['id', 'city', 'state', 'price', 'reviews'])
  r.__next__() # skip header
  for row in r:
    intprice = round(float(row['price']))

    # ensure we have the correct number of columns
    if len(row.items()) != 5 or intprice < 1 or len(row['city']) == 0 or len(row['state']) == 0:
      print('this seems to be a bogus row: {}'.format(' - '.join((row['city'], row['price'], row['reviews']))))
      #c += 1
    citystate = '{}--{}'.format(row['city'].title(), row['state'].upper())
    cityvals[citystate].append(intprice)
    if c > 5: break

c=0
citymedians = collections.defaultdict(list)
for row in sorted(cityvals.items(), key=lambda x: len(x[1]), reverse=True)[:100]:
  citymedians[row[0]] = (round(statistics.median(row[1])), len(row[1]), round(statistics.pstdev(row[1])))

print(','.join(('city', 'state', 'price median', 'listings', 'price stddev')))
for row in sorted(citymedians.items(), key=lambda x: x[1], reverse=True):
  c += 1
  #if c > 5: break
  splitcity = row[0].split('--')
  print(','.join(splitcity) + ',' + ','.join([str(x) for x in row[1]]))

