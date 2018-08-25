# DomeFlats_1.2p

## Version 1

2018-07-05, Robert Lupton: You wouldn't usually bother, just take enough flats that the counts were 100\* the sky (so 50\* or 200\* wouldn't be important!).   We can probably use 10\*sky, or a 5% loss in SN.  Maybe 5\*sky (10%).  I did that right, didn't I?

2018-07-06, Jim Chiang: ok, here are e-/pixel values (assuming 0.2"x0.2" pixels) for two locations on the sky, one at the center of the full protoDC2 region (WFD_center) and the other at the center of the uDDF region, integrated over all of the Run1.2p visits:

```
band   WFD_center   uDDF_center
 u            975         17960
 g           6738        268346
 r          34578        222485
 i          43131        167237
 z          54132        209513
 y          54756        236889
```

## Version 2

[Expected Sky Counts (Javier Sanchez)](https://github.com/lsst-pst/syseng_throughputs/blob/master/notebooks/Syseng%20Throughputs%20Repo%20Demo.ipynb)

band | skyCounts
---- | ---------
u | 70.402589
g | 406.358769
r | 812.576131
i | 1144.015607
z | 1715.474293
y | 2283.488487

2018-07-06, Jim Chiang:
```
band   min   mean    median    max
u       55    112       107    267
g      358   1686       691  11411
r      450   1352       922   6226
i      388   1300      1144   3791
z      662   1553      1541   3177
y      548   1750      1785   3100
```

## Resource Estimation

[Google Sheet Calculator](https://docs.google.com/spreadsheets/d/1ZC6ByCW_KctBI0Q6F12gVjzPJs3mzbUTJGJPALKy2qw/edit?usp=sharing)

## Scheduling

[Theta queue policy](https://www.alcf.anl.gov/user-guides/job-scheduling-policy-xc40-systems#queues):
* node count >= 128 nodes (minimum  allocation): maximum 3:00:00 hours
* node count >= 256 nodes : maximum 6:00:00 hours
* node count >= 384 nodes : maximum 9:00:00 hours
* node count >= 640 nodes : maximum 12:00:00 hours
* node count >= 802 nodes (648 nodes 2018 INCITE) : maximum 24:00:00 hours

visits | nodes
------ | -----
1 | 189
2 | 378
3 | 567
4 | 756
5 | 945
6 | 1134

Runtime:
* 1,000 e-/pixel: ~40-45 min, 189 nodes (3 hrs) x 3 sensor visits per node
* 10,000 e-/pixel: ~6 hrs, 3\*189 = 567 nodes (9 hrs) x 1 sensor visit per node
