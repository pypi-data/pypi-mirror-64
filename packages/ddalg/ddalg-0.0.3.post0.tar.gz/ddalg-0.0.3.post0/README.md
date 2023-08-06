# ddalg
Algorithms and data structures for my Python projects.

[![Build Status](https://travis-ci.org/ielis/ddalg.svg?branch=master)](https://travis-ci.org/ielis/ddalg)

## Interval tree

Interval tree is a data structure for holding intervals and to allow efficiently find intervals that overlap with given interval or point. Read more on [Wikipedia](https://en.wikipedia.org/wiki/Interval_tree).

### Implementation note
This implementation uses half-open intervals, where begin coordinate is excluded. Half-open intervals are used in e.g. [BED genomic format](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).

The current implementation needs to rebuild the tree after each `insert`, hence the tree is not efficient for using in *read/write* fashion.

### Usage

- implement your custom interval object while extending `Interval`. Two properties need to be overwritten:
  - `begin` - 0-based (excluded) begin coordinate of the interval
  - `end` - 0-based (included) end coordinate of the interval
    ```python
    from ddalg.model import Interval
    
    class YourInterval(Interval):
    
      def __init__(self, begin: int, end: int):
        self._begin = begin
        self._end = end
        # anything else
    
      @property
      def begin(self):
        return self._begin
    
      @property
      def end(self):
        return self._end
    ``` 
- create a collection of your intervals and store them in the interval tree:
  ```python
  from ddalg.itree import IntervalTree
   
  itree = IntervalTree([YourInterval(0, 3), YourInterval(1, 4)])
  # ... 
  ```
- query `itree`:
  - using 1-based *position*:
    ```python
    itree.search(1)
    ```
    > returns `(0,3)`
  - using half-open *interval coordinates*:
    ```python
    itree.get_overlaps(0, 1) 
    ``` 
    > returns `(0,3)`, effectively the same query as above
  - for intervals with minimal required coverage
    ```python
    itree.fuzzy_query(0, 1, coverage=.90)
    ```
    > return intervals with >=.9 overlap with respect to query coordinates 
  - for intervals with minimal jaccard index
    ```python
    itree.jaccard_query(0, 1, min_jaccard=.90)
    ```
    > return intervals having jaccard_index>=.9 with respect to query coordinates 