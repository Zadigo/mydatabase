## Commands

```Shell
# List of the top 10 slowest-running tests
pytest --durations=10

# Find heavy slow-loading third-party libraries that drag down execution
python -X importtime -m pytest
```
