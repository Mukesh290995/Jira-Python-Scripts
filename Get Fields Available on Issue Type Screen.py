import http.client
import base64
import json
import csv
import os

# === Replace with your actual credentials ===
EMAIL = "USER_MAIL"
API_TOKEN = "<API Token>"
BASE_URL = "domain.atlassian.net"
ISSUE_TYPE_ID = "11404" //issuetype ID

PROJECT_KEYS = [
    "ADV",
"BMK",
"CFM",
"COM",
"CMU",
"LST",
"SPACE",
"VL",
"VOICE"
] 

# === Basic Auth Header ===
auth = f"{EMAIL}:{API_TOKEN}"
auth_bytes = auth.encode("utf-8")
auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

headers = {
    "Authorization": f"Basic {auth_b64}",
    "Accept": "application/json"
}

# === Create Output Folder ===
output_dir = "jira_create_meta_csv"
os.makedirs(output_dir, exist_ok=True)

# === Start Connection ===
conn = http.client.HTTPSConnection(BASE_URL)

for project in PROJECT_KEYS:
    print(f"\n🔍 Fetching fields for project: {project}")
    fields_data = []
    start_at = 0
    total = 1  # Dummy to start loop

    while start_at < total:
        path = f"/rest/api/3/issue/createmeta/{project}/issuetypes/{ISSUE_TYPE_ID}?startAt={start_at}"
        conn.request("GET", path, headers=headers)
        response = conn.getresponse()
        body = response.read().decode("utf-8")

        if response.status != 200:
            print(f"❌ Error for {project} (HTTP {response.status}): {response.reason}")
            break

        data = json.loads(body)
        total = data.get("total", 0)
        start_at += data.get("maxResults", 50)

        fields = data.get("fields", [])
        for field in fields:
            fields_data.append({
                "Field Name": field.get("name", ""),
                "Required": field.get("required", False)
            })

    # === Write CSV for this project ===
    if fields_data:
        filename = os.path.join(output_dir, f"{project}.csv")
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Field Name", "Required"])
            writer.writeheader()
            writer.writerows(fields_data)
        print(f"✅ Saved: {filename}")
    else:
        print(f"⚠️ No fields found for project: {project}")

conn.close()
print("\n🎉 Done. CSV files saved in:", output_dir)
