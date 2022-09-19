import requests

base_url = 'https://webexapis.com/v1'
bearer_token = 'MjE0MWNhMzYtYjRmZC00NDJkLTlmYWItOTRlYmZhY2FjY2MzNGZmNTRmOWMtMmVl_P0A1_472b73d0-cdae-43f5-a538-585884a4bb41'

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token}",
}

webhook = {
    "name": "My Awesome Webhook",
    "targetUrl": "https://9dfb-98-97-39-250.ngrok.io/webhook",
    "resource": "messages",
    "filter": "mentionedPeople=me",
    "event": "created",
}

#read current webhooks and delete them as a cleanup
response = requests.get(f"{base_url}/webhooks", headers=headers, json=webhook)
response.raise_for_status()

#delete them one by one
for item in response.json()['items']:
    print(f"Deleting webhook {item['name']}...")
    delete_item = requests.delete(f'{base_url}/webhooks/{item["id"]}', headers=headers)
    delete_item.raise_for_status()
    print (delete_item.status_code)

#create a new one
response = requests.post(f"{base_url}/webhooks", headers=headers, json=webhook)
response.raise_for_status()

webhook_id = response.json()["id"]
print(f"Webhook for {webhook['targetUrl']} added with ID\n{webhook_id}")