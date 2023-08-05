<div style="text-align: center">
    <h1 > Melting Geos </h1>
    
</div>

<div id="badges" align="center">

  [![](https://img.shields.io/badge/version-0.0.1-orange.svg)](#)
  [![](https://img.shields.io/badge/sqlite-3-red.svg)](#)
  [![](https://img.shields.io/badge/python3-16.12+-blue)](#)

</div>

## Introduction
Find standard city names by obfuscated names;

## How to use

```bash
git clone https://github.com/arrebole/meltingGeos.git;
cd meltingGeos;
```

```bash
python  ./meltingGeos.py --search 北京 --depth 1
# out: [(type: 'province'', code: '11'', name: '北京市')]
```

```bash
python  ./meltingGeos.py --search 宁波 --depth 2
# out [(type: 'city'', code: '3302'', name: '宁波市')]
```


```bash
python  ./meltingGeos.py --search 鄞州 --depth 3
# out [(type: 'area'', code: '330212'', name: '鄞州区')]
```

```bash
python  ./meltingGeos.py --search 北 --depth 1
# [(type: 'province'', code: '11'', name: '北京市'), 
# (type: 'province'', code: '13'', name: '河北省'), 
# (type: 'province'', code: '42'', name: '湖北省')]
```

or lib

```python
from meltingGeos.libgs import Geos

Geos().findall("鄞州", depth = 3)
# [{type: 'area'', code: '330212'', name: '鄞州区'}]

Geos().findone("鄞州", depth = 3)
# is object no dict
# {type: 'area'', code: '330212'', name: '鄞州区'}

```