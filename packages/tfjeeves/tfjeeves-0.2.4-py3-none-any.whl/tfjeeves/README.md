# tfkit

tfkit contains a number of callbacks to help with training using tf2/keras

```python
from tfkit import StopTrainingOnSuccess

st = StopTraining(0.99)
model.fit(..., callbacks=[st, ...], ...)
```
