# xvgpy
### A scriptable vector graphics library for Python

---
## **Install** 
```
python3 -m pip install xvg
```
(See: [PyPI package](https://pypi.org/project/xvg/))

---
## **Example** 
```python
from xvg.application import Engine
from xvg.renderers import SVGRenderer

Engine(SVGRenderer()).processFile('image.xvg')
```
(See: [Test Examples](xvg/tests))

(See: [XVG Reference](xvg/tests))

---