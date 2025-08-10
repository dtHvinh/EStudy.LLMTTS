import http.client
import json
import ssl

conn = http.client.HTTPSConnection(
    "localhost", 7185, context=ssl._create_unverified_context()
)

conn.request("GET", f"/api/ai/conversations/{2}")

responseBody = conn.getresponse().read()
conversationDetails = json.loads(responseBody.decode("utf-8"))

context = conversationDetails.get("context", "")

conn.close()

print(context)
