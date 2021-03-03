

Usage

```sh
python3 conversion.py  currency-conversion.cs
pytest --benchmark-disable --capture=no --verbose --maxfail=1 .

```

Example of output 

```sh
Currency converter
1  100.0ILS to USD  rate 0.3029722922 total 30.29722922USD
2  150.0USD to GBP  rate 0.7185982707 total 107.789740605GBP
3  200.0USD to EUR  rate 0.8313934154 total 166.27868308EUR
4 from BOB to USD sum 300.0 conversion failed Got status 400 from https://api.exchangeratesapi.io/latest?base=BOB&symbols=USD
5  50.0CAD to USD  rate 0.7900164204 total 39.50082102USD
```