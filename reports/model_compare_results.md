# Search Model Comparison

Jobs: 5000. Test profiles: 20. Tool searches: 23.

| Measure | MiniLM (current) | BGE small |
|---|---|---|
| Role + skills: profiles with 1+ relevant job | 20 / 20 (100%) | 20 / 20 (100%) |
| Role + skills: relevant jobs | 97 / 100 (97%) | 100 / 100 (100%) |
| Skills only: profiles with 1+ relevant job | 18 / 20 (90%) | 20 / 20 (100%) |
| Skills only: relevant jobs | 86 / 100 (86%) | 97 / 100 (97%) |
| Skills only: relevant AND Fresher or Junior | 57 / 100 (57%) | 46 / 100 (46%) |
| Exact tools: searches with 1+ job listing ALL tools | 20 / 23 (87%) | 21 / 23 (91%) |
| Exact tools: jobs listing ALL tools | 91 / 115 (79%) | 87 / 115 (76%) |
| Time to turn all jobs into numbers | 27 seconds | 53 seconds |
| Average time per search | 8 ms | 12 ms |
| Length of each job's list of numbers | 384 | 384 |