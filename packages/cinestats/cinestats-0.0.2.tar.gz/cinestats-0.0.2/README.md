# cinestats ![Test](https://github.com/lkluft/cinestats/workflows/Test/badge.svg)
Analyse and visualise statistics around movies and cinema.

## Installation and requirements
Cinestats requires Python version 3.5 or higher.
You can install the cloned working copy using ``pip``:
```bash
$ git clone https://github.com/atmtools/typhon.git
$ pip install cinestats
```

## Testing
Tests can be run on the command line using [pytest]:
```bash
$ pytest --pyargs cinestats
```

## Usage
Cinestats is build around the `MovieDatabase` class. It combines all
functionality to work on sets of movies.
```python
import matplotlib.pyplot as plt
from cinestats import MovieDatabase


mdb = MovieDatabase.from_csv('cinestats/data/example.csv')

fig, ax = plt.subplots()
mdb.plot_marker()
plt.show()
```

### CSV data format
Movie databases can be stored as CSV file. Currently, the two fields `date` and
`movie` are supported:
```
date,movie
2017-01-01,Shaun of the Dead
2017-01-03,World's End
2017-01-02,Hot Fuzz
```

[Anaconda]: https://www.continuum.io/downloads
[pytest]: https://docs.pytest.org/en/latest/
