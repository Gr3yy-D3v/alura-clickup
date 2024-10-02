import requests

list_id = "901105126642"
url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

query = {
  "custom_task_ids": "true",
  "team_id": "123"
}

payload = {
  "name": "New Task Name",
  "description": "New Task Description",
  "markdown_description": "New Task Description",
  "assignees": [
    183
  ],
  "archived": False,
  "group_assignees": [
    "dd01f92f-48ca-446d-88a1-0beb0e8f5f14"
  ],
  "tags": [
    "tag name 1"
  ],
  "status": "Open",
  "priority": 3,
  "due_date": 1508369194377,
  "due_date_time": False,
  "time_estimate": 8640000,
  "start_date": 1567780450202,
  "start_date_time": False,
  "points": 3,
  "notify_all": True,
  "parent": None,
  "links_to": None,
  "check_required_custom_fields": True,
  "custom_fields": [
    {
      "id": "9011365192",
      "value": "This is a string of text added to a Custom Field."
    }
  ]
}

headers = {
  "Content-Type": "application/json",
  "Authorization": "pk_2142600060_YMK5RONMHWA264K0Y0J8HC7AO9N90UZ6"
}

response = requests.post(url, json=payload, headers=headers, params=query)

data = response.json()
print(data)