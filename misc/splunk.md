Splunk Refs
==============


Pull out a new field

```
| rex field=<NAME> "(?<NAME>[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
```


Group by a field

```
# Just grab unique values for it
| dedup <NAME>

# Actualy group and count them
| stats count by <NAME>
```

