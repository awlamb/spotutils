#USAGE
```python
>>> from spotutils import Cluster
>>> cluster = Cluster(key='production',access_key_id='',secret_key_id='')
>>> cluster.launch()
>>> cluster.fleet_id
'sfr-eef4a723-82ed-49b9-be27-f20545641fec'
>>> cluster.cancel_fleet_request(cluster.fleet_id)
{'ResponseMetadata': {'RequestId': '73e8b605-f408-4b9f-a85a-b25377ef41bd', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'server': 'AmazonEC2', 'date': 'Wed, 27 Jul 2016 23:35:39 GMT', 'vary': 'Accept-Encoding'}}, 'SuccessfulFleetRequests': [{'PreviousSpotFleetRequestState': 'submitted', 'CurrentSpotFleetRequestState': 'cancelled_terminating', 'SpotFleetRequestId': 'sfr-eef4a723-82ed-49b9-be27-f20545641fec'}], 'UnsuccessfulFleetRequests': []}
```
#TODO:
*Add mocks and tests with VCR

*Error checking

*function for fleet description
