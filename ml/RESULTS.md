# THREE-WAY 
response High Low Med
    High  231  82 112
    Low    73 189  93
    Med    85  95 142

> sum(ml_df$elo == "Low")
[1] 366
> sum(ml_df$elo == "High")
[1] 389
> sum(ml_df$elo == "Med")
[1] 347

  LO_BINS  HI_BINS NUM_TRAIN NUM_TEST TOTAL_SIZE               MODEL       ACCURACY
1   1-2-3 7-8-9-10       881      221       1102      classif.ranger 0.5780543
2   1-2-3 7-8-9-10       881      221       1102      classif.ranger 0.5753682
3   1-2-3 7-8-9-10       881      221       1102        classif.kknn 0.5099548
4   1-2-3 7-8-9-10       881      221       1102        classif.kknn 0.4981530
5   1-2-3 7-8-9-10       881      221       1102         classif.qda 0.4682353
6   1-2-3 7-8-9-10       881      221       1102         classif.qda 0.4673097
7   1-2-3 7-8-9-10       881      221       1102 classif.naive_bayes 0.4019334
8   1-2-3 7-8-9-10       881      221       1102 classif.naive_bayes 0.3956314

# THIRD RUN 
     LO_BINS    HI_BINS NUM_TRAIN NUM_TEST TOTAL_SIZE               MODEL       AUC
1          1         10       161       41        202      classif.ranger 0.8733822
2          1         10       161       41        202         classif.qda 0.8494169
3        1-2       9-10       342       86        428      classif.ranger 0.8489111
4      1-2-3     8-9-10       548      137        685      classif.ranger 0.8312603
5          1         10       161       41        202        classif.kknn 0.8195990
6          1         10       161       41        202     classif.log_reg 0.8153094
7        1-2       9-10       342       86        428         classif.qda 0.8080099
8    1-2-3-4   7-8-9-10       719      180        899      classif.ranger 0.7907249
9        1-2       9-10       342       86        428        classif.kknn 0.7878076
10     1-2-3     8-9-10       548      137        685        classif.kknn 0.7824066
11       1-2       9-10       342       86        428     classif.log_reg 0.7691261
12         1         10       161       41        202 classif.naive_bayes 0.7672581
13 1-2-3-4-5 6-7-8-9-10       881      221       1102      classif.ranger 0.7530929
14     1-2-3     8-9-10       548      137        685         classif.qda 0.7494512
15   1-2-3-4   7-8-9-10       719      180        899        classif.kknn 0.7271588
16     1-2-3     8-9-10       548      137        685     classif.log_reg 0.7141102
17   1-2-3-4   7-8-9-10       719      180        899         classif.qda 0.7029497
18 1-2-3-4-5 6-7-8-9-10       881      221       1102        classif.kknn 0.6912109
19       1-2       9-10       342       86        428 classif.naive_bayes 0.6868680
20 1-2-3-4-5 6-7-8-9-10       881      221       1102         classif.qda 0.6847636
21   1-2-3-4   7-8-9-10       719      180        899     classif.log_reg 0.6802622
22 1-2-3-4-5 6-7-8-9-10       881      221       1102     classif.log_reg 0.6493108
23     1-2-3     8-9-10       548      137        685 classif.naive_bayes 0.6395624
24   1-2-3-4   7-8-9-10       719      180        899 classif.naive_bayes 0.6322420
25 1-2-3-4-5 6-7-8-9-10       881      221       1102 classif.naive_bayes 0.5951622

# SECOND RUN
     LO_BINS    HI_BINS               MODEL       AUC
1        1-2       9-10      classif.ranger 0.8807975
2          1         10      classif.ranger 0.8807524
3          1         10        classif.kknn 0.8473054
4      1-2-3     8-9-10      classif.ranger 0.8206561
5    1-2-3-4   7-8-9-10      classif.ranger 0.8183239
6          1         10     classif.log_reg 0.8139333
7        1-2       9-10        classif.kknn 0.8106312
8          1         10         classif.qda 0.8033891
9        1-2       9-10         classif.qda 0.7949264
10     1-2-3     8-9-10        classif.kknn 0.7815258
11 1-2-3-4-5 6-7-8-9-10      classif.ranger 0.7667529
12       1-2       9-10     classif.log_reg 0.7578612
13     1-2-3     8-9-10         classif.qda 0.7480618
14         1         10 classif.naive_bayes 0.7352640
15   1-2-3-4   7-8-9-10         classif.qda 0.7167017
16   1-2-3-4   7-8-9-10        classif.kknn 0.7126758
17   1-2-3-4   7-8-9-10     classif.log_reg 0.6923346
18     1-2-3     8-9-10     classif.log_reg 0.6901573
19 1-2-3-4-5 6-7-8-9-10         classif.qda 0.6850600
20 1-2-3-4-5 6-7-8-9-10        classif.kknn 0.6798117
21       1-2       9-10 classif.naive_bayes 0.6775144
22 1-2-3-4-5 6-7-8-9-10     classif.log_reg 0.6510582
23     1-2-3     8-9-10 classif.naive_bayes 0.6471014
24   1-2-3-4   7-8-9-10 classif.naive_bayes 0.6306744
25 1-2-3-4-5 6-7-8-9-10 classif.naive_bayes 0.5994426


# FIRST RUN
|  |   LO_BINS|    HI_BINS |         MODEL   |    AUC|
|--|----------|-----------|---------------|----------|
|1 |         1|         10|    classif.qda| 0.8845688|
|2 |         1|         10| classif.ranger| 0.8703839|
|3 |       1-2|       9-10| classif.ranger| 0.8633731|
|4 |         1|         10|    classif.lda| 0.8273026|
|5 |     1-2-3|     8-9-10| classif.ranger| 0.8228175|
|6 |         1|         10|    classif.svm| 0.8169273|
|7 |   1-2-3-4|   7-8-9-10| classif.ranger| 0.8053695|
|8 |       1-2|       9-10|    classif.qda| 0.7925613|
|9 |       1-2|       9-10|    classif.lda| 0.7856250|
|10| 1-2-3-4-5| 6-7-8-9-10| classif.ranger| 0.7539548|
|11|       1-2|       9-10|    classif.svm| 0.7528306|
|12|     1-2-3|     8-9-10|    classif.qda| 0.7519487|
|13|     1-2-3|     8-9-10|    classif.svm| 0.7293297|
|14|   1-2-3-4|   7-8-9-10|    classif.qda| 0.7028487|
|15|     1-2-3|     8-9-10|    classif.lda| 0.6958069|
|16|   1-2-3-4|   7-8-9-10|    classif.lda| 0.6883419|
|17|   1-2-3-4|   7-8-9-10|    classif.svm| 0.6744187|
|18| 1-2-3-4-5| 6-7-8-9-10|    classif.qda| 0.6682413|
|19| 1-2-3-4-5| 6-7-8-9-10|    classif.lda| 0.6619092|
|20| 1-2-3-4-5| 6-7-8-9-10|    classif.svm| 0.6368331|