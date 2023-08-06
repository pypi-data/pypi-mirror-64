# Picture Cutter

This library reads an PIL Image and returns some Images (defined by some boundaries).

# Remarks

Pre-Alpha. Do not use it.

# Reminder for myself on how to package and upload a python package

[https://packaging.python.org/tutorials/packaging-projects/]

It's probably editing the version in setup.py and then

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

Should then be installable via `pip install picture_cutter`
