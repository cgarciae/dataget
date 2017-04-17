# dataget

## Example
### Simple
Using bash
```bash
dataget load german-traffic-signs #download, extract and cleanup folder
dataget process german-traffic-signs #process (convert to 32x32 jpg)
```
Using python
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder
signs.load().process() #process (convert to 32x32 jpg)
```

### More control
Using bash
```bash
dataget download german-traffic-signs #download
dataget extract german-traffic-signs #extract
dataget remove-sources german-traffic-signs #cleanup folder
dataget process german-traffic-signs #process (convert to 32x32 jpg)
```

Using python
```python
from dataget import data
signs = data("german-traffic-signs")
signs.download() #download
signs.extract() #extract
signs.remove_sources() #cleanup folder
signs.process() #process (convert to 32x32 jpg)
```

### Params
Using bash
```bash
dataget process german-traffic-signs -p dims:40x40 #process (convert to 40x40 jpg)
```
Using python
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder
signs.process(dims="40x40") #process (convert to 32x32 jpg)
```

### Numpy and Pandas
Assuming you already downloaded the data, you can
```python
from dataget import data
signs = data("german-traffic-signs") #download, extract and cleanup folder

df = signs.training_set.datafame()
```
