# Cryptoscore

In place of a traditional RDMBS or NoSQL database, this flat file is used. Currently wondering if its just better to go with a real DB though...

In terms of general format, the data is structured in an array of timepoints.

> I.E. the 0th element of the array corresponds to time_delta 0. The 100th element corresponds to time delta 100 (hours) and so forth.

Each index in the array contains 20 dict's mapped to each tracked currency.
> The first index will store twitter_score, the second index will store reddit_score.

```
[
  (t_delta 0) [
    (crypto_0) [0,0],
    (crypto_1) [0,0],

    ...

  ],
  (t_delta 1) [
    (crypto_0) [0,0],
    (crypto_1) [0,0],

    ...

  ],

  ...

  (t_delta 719) [
    (crypto_0) [0,0],
    (crypto_1) [0,0],

    ...

  ],
]
```

So once you load this dataset into memory, this pseudocode will give you a general sense...

```
import json

data = json.load(open('cryptocurrencies/cryptoscore.json'))

# To access the twitter score of ripple on the 12th hour since data collection. (Arrays start at 0, so watch for off by one errors).

data[11]['ripple'][0]
```
