
# Thesaurus Query Expansion Evaluation

**Project Source Code:** [https://github.com/Navnedia/Building-A-Search-Engine](https://github.com/Navnedia/Building-A-Search-Engine)

<!--

| Number of Results | 1      | 10     | 25     | 50     | 75     | 100    |
| ----------------- | :----: | :----: | :----: | :----: | :----: | :----: |
| **Before**        | 34     | 341    | 761    | 1,330  | 1,824  | 2,291  |
| **After**         | 46     | 446    | 1,050  | 1,871  | 2,488  | 3,078  |
| **Improvement**   | 12     | 105    | 289    | 541    | 664    | 7,687  |
| **Improve (%)**   | 35.29% | 30.79% | 37.97% | 40.67% | 36.40% | 34.35% |

-->

![Table of testing results](https://user-images.githubusercontent.com/87249556/224840648-c9a22435-b608-4d56-bd55-395940d952ef.png)

![Graph of testing results](https://user-images.githubusercontent.com/87249556/224837348-77e1eb4a-8d01-4485-aafb-ae31d0096853.png)

After I finished adding synonym query expansion I wanted to see if it improved the search result relevance. To do this I tested the search
engine before and after query expansion and compared the results against a large set of human evaluations. For testing, I ran the evaluation
tests for several different numbers of expected results asking for just 1 result, and up to 100 results. 

My testing showed a consistent improvement in relevancy scores across all tests. This means that the results have become more relevant based
on human evaluation because we are able to consider related words that a human might also find to be relevant to their search. Before I had a
score of 341 when looking at 10 results, but after running the query expansion, the score jumped up to 446; this was an increase of 30.79% in
result relevancy. Similarly, for 100 results, beforehand I had a score of 2,291, but after, I got a score of 3,078; this was an increase of 34.35%.

All test improvements ranged from 30 to 40 percent increases, meaning the average increase in relevance with my test data set was 35.91%. These
significant increases show that the query expansion implementation was impactful in returning more relevant results.
