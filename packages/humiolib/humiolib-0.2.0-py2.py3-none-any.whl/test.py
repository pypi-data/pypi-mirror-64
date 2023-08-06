from humiolib.HumioClient import HumioClient, HumioIngestClient
import time
client = HumioClient(
        base_url= "https://cloud.humio.com",
        repository= "sandbox",
        user_token="ddDQnNHKCj6PY7YyU4OT4A9pT79gVzqltllnLjSUCEE5",
    )



"""
queryjob = client.init_queryjob("timechart()", is_live=True)

for pollResult in queryjob.poll_until_done():
        for x in pollResult.events:
                print(x)
        print("NEXT POLL")
        
print(queryjob.is_done)

for pollResult in queryjob.poll_until_done():
        for x in pollResult.events:
                print(x)
        print("NEXT POLL")


socket = client._streaming_query("timechart()", is_live=True)
for x in socket:
    print(x)

print("Wool")

for pollResult in queryjob.poll_until_done():
        for x in pollResult.events:
                print(x)
        print("NEXT POLL")
        
print(queryjob.is_done)

while True:
        pollResult = queryjob.poll()
        for event in pollResult.events:
                print(event)


print(client.get_status())
#print(client.get_status_json())

print(client)
print(HumioClient._from_saved_state(client._state))

"""

ingest_client = HumioIngestClient(  base_url= "https://cloud.humio.com",
        ingest_token="Lpc4hoaLATgWNiUkdUTN1qA6Ocl1zqPx6jAG8xVW2Npy",)


messages = [

"192.168.1.21 - user1 [02/Nov/2017:13:48:26 +0000] \"POST /humio/api/v1/ingest/elastic-bulk HTTP/1.1\" 200 0 \"-\" \"useragent\" 0.015 664 0.015",
"192.168.1.49 - user1 [02/Nov/2017:13:48:33 +0000] \"POST /humio/api/v1/ingest/elastic-bulk HTTP/1.1\" 200 0 \"-\" \"useragent\" 0.014 657 0.014",
"192.168.1..21 - user2 [02/Nov/2017:13:49:09 +0000] \"POST /humio/api/v1/ingest/elastic-bulk HTTP/1.1\" 200 0 \"-\" \"useragent\" 0.013 565 0.013",
"192.168.1.54 - user1 [02/Nov/2017:13:49:10 +0000] \"POST /humio/api/v1/ingest/elastic-bulk HTTP/1.1\" 200 0 \"-\" \"useragent\" 0.015 650 0.015"

]

#client._ingest_messages(messages)


j = [
  {
    "tags": {
      "host": "server1",
      "source": "application.log",
      "type": "json"
    },
    "events": [
      {
        "timestamp": "2020-03-23T00:00:00+00:00",
        "attributes": {
          "key1": "value1",
          "key2": "value2"
        },
        "rawstring": "starting service coordinator"        
      },
      {
        "timestamp": "2020-03-23T00:00:00+00:00",
        "attributes": {
          "key1": "value1"
        },
        "rawstring": "starting service coordinator"
      }
    ]
  }
]

client.ingest_json_data(j)
ingest_client.ingest_json_data(j)