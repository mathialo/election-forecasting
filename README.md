# Election Forecasting

Playing around with election models for the Norwegian 2021 election

Run the model by running 
```
$ poetry run model <simulations>
```

The model uses polling data from all 19 electoral districts to predict the election result of each districts, and runs
the modified Sainte-Lagüe's method on each district to figure out the distribution of electorates. It then presents a
report of findings.
