# pyfreewheel

## Description
Communicate with the [Freewheel inbound API](https://hub.freewheel.tv/display/SSPTW/Inbound+API): retrieve, create, and update information on sites, publishers, zones, etc.

## Usage
Call `freewheel.API()` with your inbound API key as the only positional argument to create an API object with functions `retrieve(<endpoint>)`, `update(<endpoint>)`, `create(<endpoint>)`, corresponding to `GET`, `PUT`, and `POST` respectively.

```python
#import freewheel
FW_API_KEY = '<inbound api key>'
fw = freewheel.API(FW_API_KEY)
sites = fw.request('site')
print(sites.results)

example_zone = fw.request('zone', id=123456)
sid = example_zone.results['site_id']
updated = fw.update('site', {'name': 'New Name'}, id=sid)
print(updated.results)
```
