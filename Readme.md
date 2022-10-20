# Modified N - Puzzle Problem


```bash
.\modified_n_puzzle.exe -h
```
```
usage: modified_n_puzzle.exe [-h] [--heuristic misplaced/manhattan] [--time TIME]
                             Start-Configuration Goal-Configuration

Modified N Puzzle Problem

positional arguments:
  Start-Configuration   Text file containing start configuration of puzzle
  Goal-Configuration    Text file containing goal configuration of puzzle

optional arguments:
  -h, --help            show this help message and exit
  --heuristic misplaced/manhattan
  --time TIME
```

### Content
* `modified_n_puzzle.py` - script to solve the problem 
* `generate_and_test.py` - script for generating the configurations 
                           and write the results to `result.txt`( nodes checked using manhattan heuristic and misplace heuristic function) 
* `/test data` - folder contains the configurations used for the analysis
* `analysis.ipynb` - Jupyter notebook for analysing data and perform paired t-test