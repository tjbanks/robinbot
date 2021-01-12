# robinbot
A Robinhood crypto trading bot powered by machine learning

### Collecting data
```
robinbot -u yourusername run recorder
```

### Labeling CSV data collected
```
robinbot data --csv DOGE.csv label --output-file DOGE_labeled1.csv default --column-name mark_price --rolling-mean 10 --window-size 70
```

### Training a network:
Test command:
```
robinbot data -c DOGE_labeled1.csv -x ask_price,bid_price,mark_price -y labels train --epochs 10 --batch-size 10 lstm --lookback 300 --lookback-skip 1 --every-other-hold 15
```

### Trading with a trained network:
TBD