In REPL [Scripting > Console (REPL)]:
```python
def rec(start, prefixes=[]):
    if len(prefixes) >= 5: return
    if start in (talon.track.tobii, talon.skia, talon.ui, None, os, sys): return
    if type(start) in (int, str, float, bool): return
    for key in dir(start):
        if key == '__getstate__': continue
        if key.startswith('whisper_'): continue
        # if 'get' in key and key not in ('__getitem__', '__getattribute__', '__class_getitem__'): print(prefixes, key)
        if 'active' in key: print(prefixes, key)
        # if 'mode' in key and key not in ('modes',): print(prefixes, key)
        # if 'enabled' in key: print(prefixes, key)
        if key.startswith('_'): continue
        try:
            value = getattr(start, key)
            if callable(value): continue
            rec(value, prefixes + [key])
        except Exception as e:
            print(f"Error accessing {key} on {start}: {e}")

rec(talon)
```

