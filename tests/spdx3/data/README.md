# Serialization Test Data

The test configuration [Payloads.md](Payloads.md) is a markdown file with a list of payloads to be generated
and checked against the expected result.  Each test is a level2 heading containing the expected payload path
followed by the element paths used to construct the payload:
```
## <format>/payloads/<filename>
- <format>/elements/<file1>
- <format>/elements/<file2>
- <format>/elements/<file3>
```

The formats do not need to match - an RDF payload can be constructed from a mix of different element formats
as long as the element reader and payload writer formats exist.
