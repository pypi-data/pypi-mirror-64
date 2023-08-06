
## BITCOIN PRICE NOTIFICATION 

A Python script package to get the  bitcoin price notifications on regular interval.  

Using this project any one can get the regular updated price of bitcoin at a some time interval. Which you can set by yourself while running the program or the default value of the interval is 1 minute which means that by default after every five minutes you will get the updated price!!!. You will get the price notification on telegram for that you have to join the channel.


## Installation

Following command on terminal will install bitcoin-notifier package/module from PIP

```bash
pip install habib-bitcoin-price
```

## Usage

Following query on terminal will provide you with all the help options available

### Input 

```bash
habib-bitcoin-price -h
```

### Output 

```

usage: habib-bitcoin-price [-h] [--d D] [--i I] [--u U]

Bitcoin price notification alert

optional arguments:
  -h, --help            show this help message and exit
  --d D                 Enter (Yes/No) to run the bitcoin notification
  --i I, --interval I   Time interval for updated price in minutes in this
                        (0.1,1,2) format
  --u U, --Upper threshold U
                        Set the upper threshold limit in USD for notification

```

### Following query on terminal will provide you five prices of Bitcoin.

```bash

habib-bitcoin-price --d=Y --i=0.5 --u=10000

```

## Join this telegram channel to get the updates :

Following is the invite link

```bash
    https://t.me/Bitcoin_Price_Habib
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.
