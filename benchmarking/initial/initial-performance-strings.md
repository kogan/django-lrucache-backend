# Timings

Comparisons between the LocMem cache and our LRU cache. Keys are strings and
values are strings. Pickle isn't engaged as often when the values are strings.

Both caches are initialized with a max size of 500 entries. The 3 test cases
use a key space of 100, 500, and 1000. This demonstrates performance where
culling is non-existent, culling is sometimes visible, and culling is about
50% of operations.

The below benchmarks are generated with:

```bash
python benchmark.py -r 100 >> initial/initial-performance-strings.md
python benchmark.py -r 500 >> initial/initial-performance-strings.md
python benchmark.py -r 1000 >> initial/initial-performance-strings.md
```

LRU performs slightly better in the `delete` case. It performs slightly worse in
the `get` case in the 90th and 99th percentile, but slightly better in the median
case. LRU again performs slightly better with `set`, and massively better in the
99th percentile of `set`. The culling strategy of LocMem iterates all keys, and
adds up to the big time increases.

Overall we see LRU being consistently more performant across all strategies,
except for a small performance decrease in the 99th percentile of set.

LRU and LocMem caches should not be used in situations where there is a lot of
cache contention. Culling strategies should not be invoked at all for these
cache types. Instead, these caches should be used for small, stable, global
lookup tables.

<pre>
========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-strings-100
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712612     72319  41.962us  63.896us  81.062us  10.999ms  34.069s
      set     71464         0  46.015us  48.161us  85.115us   4.699ms   3.511s
   delete      7916         0  40.054us  41.962us  73.910us   1.651ms 334.923ms
    Total    791992                                                    37.915s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-strings-100
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712612     72319  40.054us  64.850us  82.016us  18.801ms  32.935s
      set     71464         0  41.008us  42.915us  76.056us  11.294ms   3.130s
   delete      7916         0  38.147us  40.054us  67.949us   4.608ms 323.643ms
    Total    791992                                                    36.388s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-strings-500
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827     99120  43.869us  66.042us  87.976us  11.311ms  35.578s
      set     71262         0  46.968us  50.068us  92.983us   8.014ms   3.629s
   delete      7903         0  41.008us  43.869us  78.917us   6.923ms 355.216ms
    Total    791992                                                    39.563s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-strings-500
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827     99120  41.008us  66.996us  92.983us  14.032ms  33.968s
      set     71262         0  41.962us  44.107us  81.062us  12.514ms   3.185s
   delete      7903         0  39.816us  41.008us  72.956us   3.827ms 332.599ms
    Total    791992                                                    37.485s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-strings-1000
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827    381932  63.896us  66.996us 105.143us  13.230ms  41.739s
      set     71262         0  46.015us  49.114us 475.168us   7.311ms   3.813s
   delete      7903         0  41.008us  42.915us  72.956us   2.226ms 343.023ms
    Total    791992                                                    45.894s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-strings-1000
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827    365804  57.936us  67.949us 107.050us  12.860ms  41.011s
      set     71262         0  41.962us  43.869us  72.002us   6.867ms   3.162s
   delete      7903         0  39.101us  41.008us  66.996us   2.408ms 331.898ms
    Total    791992                                                    44.504s
========= ========= ========= ========= ========= ========= ========= =========
</pre>
