# matplotlib__matplotlib-25122

**Repo:** `matplotlib/matplotlib`

## What the request must convey (all units, nothing extra)

1. `mlab._spectral_helper`: window correction computed wrong (code around `lib/matplotlib/mlab.py` L423-430)
2. `np.abs` applied to window there is unnecessary; breaks windows with negative values, e.g. `flattop`
3. reference: scipy's implementation in `scipy/signal/_spectral_py.py` (no abs)
4. repro [[A1]]: compares squared sum with/without `np.abs` for `signal.windows.flattop(512)`
5. actual output `4372.942556173262`, expected `0`
6. affects latest Matplotlib

## Attachments (paste the placeholder where you would paste the block)

### `[[A1]]` (code)

```python
import numpy as np
from scipy import signal
window = signal.windows.flattop(512)
print(np.abs(window).sum()**2-window.sum()**2)
```
