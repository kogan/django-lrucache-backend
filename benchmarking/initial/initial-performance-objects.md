# Timings

Comparisons between the LocMem cache and our LRU cache. Keys are strings and
values are thin object wrappers over strings. By utilising cProfile we can
see that pickle does consume a non-trivial amount of time, but it's not very
large.

Both caches are initialized with a max size of 500 entries. The 3 test cases
use a key space of 100, 500, and 1000. This demonstrates performance where
culling is non-existent, culling is sometimes visible, and culling is about
50% of operations.

The below benchmarks are generated with:

```bash
python benchmark.py -r 100 --complex >> initial/initial-performance-objects.md
python benchmark.py -r 500 --complex >> initial/initial-performance-objects.md
python benchmark.py -r 1000 --complex >> initial/initial-performance-objects.md
```

As expected, the LRU implementation performs slightly better in nearly all
cases. The 99th percentile shows better delete performance for the LocMem cache
when the number of entries is large - presumably because the LRU has extra
book-keeping.

The 99th percentile for both get and set favour LRU, significantly in some
cases. The culling strategy of LocMem scans the whole key space which shows
worst case performance. The LRU culling strategy shows consistent performance
across all cache sizes.

<pre>
========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-objects-100
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712612     72319  50.068us  66.996us 113.010us   7.475ms  39.539s
      set     71464         0  58.174us  63.181us 133.991us   5.219ms   4.518s
   delete      7916         0  41.962us  44.107us  80.109us   3.239ms 351.507ms
    Total    791992                                                    44.409s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-objects-100
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712612     72319  40.770us  65.804us  77.963us   9.682ms  32.534s
      set     71464         0  41.962us  43.869us  73.910us   8.645ms   3.235s
   delete      7916         0  39.816us  41.008us  61.035us   7.259ms 338.899ms
    Total    791992                                                    36.108s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-objects-500
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827     99120  51.022us  67.949us  97.036us  14.136ms  40.205s
      set     71262         0  58.889us  62.943us 118.971us  12.626ms   4.513s
   delete      7903         0  42.915us  45.061us  71.049us   2.026ms 359.551ms
    Total    791992                                                    45.078s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-objects-500
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827     99120  41.962us  67.949us  87.976us   9.464ms  34.191s
      set     71262         0  42.915us  45.061us  79.870us   6.044ms   3.255s
   delete      7903         0  41.008us  42.915us  75.817us   3.504ms 346.612ms
    Total    791992                                                    37.792s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-objects-1000
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827    382158  61.989us  68.188us 142.813us  20.156ms  47.828s
      set     71262         0  58.174us  63.896us 501.871us   6.779ms   5.076s
   delete      7903         0  41.962us  44.107us  66.042us   4.771ms 372.585ms
    Total    791992                                                    53.277s
========= ========= ========= ========= ========= ========= ========= =========

========= ========= ========= ========= ========= ========= ========= =========
Timings for lrumem-objects-1000
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712827    365804  59.843us  68.188us 112.057us  15.201ms  41.522s
      set     71262         0  42.915us  45.061us  77.963us   6.971ms   3.281s
   delete      7903         0  40.054us  41.962us  69.141us   5.482ms 352.383ms
    Total    791992                                                    45.155s
========= ========= ========= ========= ========= ========= ========= =========
</pre>
