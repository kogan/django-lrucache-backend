
<pre>
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

========= ========= ========= ========= ========= ========= ========= =========
Timings for locmem-objects-500-2.0.0
-------------------------------------------------------------------------------
   Action     Count      Miss    Median       P90       P99       Max     Total
========= ========= ========= ========= ========= ========= ========= =========
      get    712438     73137  20.981us   1.012ms   4.637ms  28.534ms 266.785s
      set     71466         0 323.057us 482.082us 844.002us  11.024ms  22.478s
   delete      8088         0 311.136us 470.161us 812.054us   2.879ms   2.433s
    Total    791992                                                   291.696s
========= ========= ========= ========= ========= ========= ========= =========

</pre>