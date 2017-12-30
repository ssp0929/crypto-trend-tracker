# Cryptolist.txt

The currencies in "cryptolist" are formatted to be compatible with the coinmarketcap API.
You may however, have to use different terminology in your scraper.

# Example

"enigma-project" is the call name on coinmarketcap api.
However, on reddit it would be referred to as only "enigma"
Similarly, "request-network" would just be "request network" on reddit.

# Cryptoscore

In place of a traditional RDMBS or NoSQL database, this flat file is used. Currently wondering if its just better to go with a real DB though...

In terms of general format, the data is structured in an array of timepoints.

> I.E. the 0th element of the array corresponds to time_delta 0. The 100th element corresponds to time delta 100 (hours) and so forth.

Each index in the array contains 20 dict's mapped to each tracked currency.

```
[
  (t_delta 0) {
    "crypto_0": {
      twitter_score: 0,
      reddit_score: 0
    },
    "crypto_1": {

      ...

    },

    ...

  },
  (t_delta 1) {

    ...

  },

  ...

  (t_delta 719) {

    ...

  }
]
```


