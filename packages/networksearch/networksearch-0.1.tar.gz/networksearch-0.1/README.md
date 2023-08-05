# Install
    pip install networksearch

# Usage

```python
>>> from networksearch.networksearch import NetworkTree
>>> tree = NetworkTree()
>>> tree.add("9.0.0.0-10.0.0.2")
>>> tree.add("192.168.0.1")
>>> tree.add("192.168.0.0/24")
>>> tree.add("192.168.0.0/22")
>>> tree.add("192.168.0.0/23")
>>> print(tree.overlaps("192.168.0.2"))
True
>>> tree.printTree()
9.0.0.0/8 
10.0.0.0/31 
10.0.0.2/32 
192.168.0.0/22 
>>>
```

# Test

    python -m unittest test/test_*.py