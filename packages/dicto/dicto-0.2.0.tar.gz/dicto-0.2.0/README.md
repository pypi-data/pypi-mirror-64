# dicto
A dict-like object that enables access of its elements as regular fields. Dicto's main feature is delivering an elegant experience while using configuration files/objects. 

### Example
You can create a Dicto from any `dict`: 

```python
import dicto

params = dicto.Dict({"learning_rate": 0.001, "batch_size": 32 })

optimizer = Adam(params.learning_rate)
```

Dicto parses through arbitrary nested structures of `dicts`, `list`, `tuple`, and `set`: 

```python
import dicto

params = dicto.Dict({
    "points":[
        {
            "x": 1,
            "y": 2
        },
        {
            "x": 3,
            "y": 4
        }
    ]
})

print(params.points[0].x) # 1
```
`dicto` can load `json`, `yaml`, and `xml` formats directly, for example, given this `YAML` file
```yaml
# params.yml
learning_rate: 0.001
batch_size: 32
```

you can load it like this:

```python
import dicto

params = dicto.load("params.yml")
optimizer = Adam(params.learning_rate)
```

## Installation
```bash
pip install dicto
```

## License
MIT License