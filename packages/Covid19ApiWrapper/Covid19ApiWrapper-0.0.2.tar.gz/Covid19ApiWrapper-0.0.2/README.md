# Covid 19 API Wrapper

## THE API CREDIT GOES TO [corona.lmao.ninja](https://github.com/NovelCOVID/API), big thanks!
### [Their Discord](https://discordapp.com/invite/EvbMshU)

## Python API Wrapper
Interacts with the API.
Hopefully this saves some people a few steps :)
Enjoy!

-------

### Without using "countries" endpoint:

```py

from Covid19ApiWrapper import *

#define the object
x = covidUpdate(BOOL_country_data=False)

print(x.totalCases)
print(x.totalDeaths)
print(x.totalRecovered)
print(x.timeUpdatedUnix)
```
-------

### Using both endpoints:
```py

from Covid19ApiWrapper import *

#define the object
x = covidUpdate(BOOL_country_data=True)

print(x.totalCases)
print(x.totalDeaths)
print(x.totalRecovered)
print(x.timeUpdatedUnix)

#Possible Usage: cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion
print(x.countryData['China']['cases'])
print(x.countryData['China']['todayCases'])

```

### Enjoy and be safe!
