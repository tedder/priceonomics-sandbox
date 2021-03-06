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
# - some outliers, like Indianapolis and Austin. Austin is an outlier for the number of entries, and Indianapolis is an outlier for the median price.

with open(sys.argv[1]) as csvfile:
  r = csv.DictReader(csvfile, fieldnames=['id', 'city', 'state', 'price', 'reviews'])
  r.__next__() # skip header
  for row in r:
    intprice = round(float(row['price']))

    # ensure we have the correct number of columns
    if len(row.items()) != 5 or intprice < 1 or len(row['city']) == 0 or len(row['state']) == 0:
      print('this seems to be a bogus row: {}'.format(' - '.join((row['city'], row['price'], row['reviews']))))

    # quick code to exclude entries with less than two reviews
    #if round(float(row['reviews'])) < 2:
    #  continue

    # making a composite key so we don't end up counting Portland Maine in the Portland Oregon bucket.
    citystate = '{}--{}'.format(row['city'].title(), row['state'].upper())
    cityvals[citystate].append(intprice)

citymedians = collections.defaultdict(list)
for row in sorted(cityvals.items(), key=lambda x: len(x[1]), reverse=True)[:100]:
  citymedians[row[0]] = (round(statistics.median(row[1])), len(row[1]), round(statistics.pstdev(row[1])))

print(','.join(('city', 'state', 'price median', 'listings', 'price stddev')))
for row in sorted(citymedians.items(), key=lambda x: x[1], reverse=True):
  splitcity = row[0].split('--')

  # weird/hacky looking code here because row[1] is a list.
  print(','.join(splitcity) + ',' + ','.join([str(x) for x in row[1]]))

