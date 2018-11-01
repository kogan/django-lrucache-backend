History
=======

2.0.0 (2018-11-01)
------------------

* Dropped support for Django < 1.11
* Updated Django support for >= 2.1
* Removed python 3.3, 3.4, and 3.5 from build matrix. Support will be best effort.
* Changed locks from a Read-Write lock to an RLock, as a read lock is incorrect for LRU algorithm
* Changed benchmark script to use threads rather than multiprocessing so that locks
  will be engaged during benchmarks.
* Now using poetry to build

Benchmarks ::

    python benchmark.py -r 500 --complex

    ========= ========= ========= ========= ========= ========= ========= =========
    Timings for lrumem-objects-500-2.0.0
    -------------------------------------------------------------------------------
    Action     Count      Miss    Median       P90       P99       Max     Total
    ========= ========= ========= ========= ========= ========= ========= =========
        get    712436     72701 159.025us 302.076us 524.044us  49.870ms 130.832s
        set     71473         0 159.979us 247.240us 470.161us  39.725ms  12.560s
    delete      8083         0 157.833us 241.756us 473.976us   6.788ms   1.397s
        Total    791992                                                   144.789s
    ========= ========= ========= ========= ========= ========= ========= =========


0.2.0 (2017-07-16)
------------------

* Don't validate the key
    - delete P90: 20% improvement
    - set P90: 17% improvement
    - get P90: 10% improvement

Benchmarks ::

    python benchmark.py -r 500 --complex

    ========= ========= ========= ========= ========= ========= ========= =========
    Timings for lrumem-objects-500-0.2.0
    -------------------------------------------------------------------------------
       Action     Count      Miss    Median       P90       P99       Max     Total
    ========= ========= ========= ========= ========= ========= ========= =========
          get    712827     99120  33.855us  59.843us  81.062us  37.626ms  28.899s
          set     71262         0  35.048us  37.909us  73.195us   5.847ms   2.719s
       delete      7903         0  32.902us  35.048us  63.896us   1.114ms 272.343ms
        Total    791992                                                    31.891s
    ========= ========= ========= ========= ========= ========= ========= =========


0.1.0 (2017-07-13)
------------------

* Project comes online

Benchmarks ::

    python benchmark.py -r 500 --complex

    ========= ========= ========= ========= ========= ========= ========= =========
    Timings for locmem-objects-500
    -------------------------------------------------------------------------------
       Action     Count      Miss    Median       P90       P99       Max     Total
    ========= ========= ========= ========= ========= ========= ========= =========
          get    712827     99120  51.022us  67.949us 127.077us  13.318ms  41.607s
          set     71262         0  59.128us  66.042us 154.018us   6.350ms   4.693s
       delete      7903         0  42.915us  46.015us  81.062us   3.040ms 361.492ms
        Total    791992                                                    46.661s
    ========= ========= ========= ========= ========= ========= ========= =========


    ========= ========= ========= ========= ========= ========= ========= =========
    Timings for lrumem-objects-500
    -------------------------------------------------------------------------------
       Action     Count      Miss    Median       P90       P99       Max     Total
    ========= ========= ========= ========= ========= ========= ========= =========
          get    712827     99120  41.008us  66.996us 102.043us  29.211ms  34.952s
          set     71262         0  42.915us  46.015us  84.162us  16.403ms   3.313s
       delete      7903         0  40.054us  43.869us  80.824us   1.426ms 340.591ms
        Total    791992                                                    38.605s
    ========= ========= ========= ========= ========= ========= ========= =========
