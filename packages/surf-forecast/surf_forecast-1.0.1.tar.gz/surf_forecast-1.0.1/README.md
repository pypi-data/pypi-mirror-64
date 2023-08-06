# surf-forecast

[![pypi](https://img.shields.io/pypi/v/surf-forecast.svg)](https://pypi.org/project/surf-forecast)

An api to fect surf forecast data

## Installation
To install the package run this command:

```bash
pip install surf-forecast
```

## Usage

### getCity

```python
from surf_forecast import fetch

getCity("Sao Conrado")

/*
{"city": "são conrado",
 "unit": "celsius",
 "temp": 26.0,
 "temp_mean": 26.1,
 "temp_min": 24.8,
 "temp_max": 27.2
} */
```



