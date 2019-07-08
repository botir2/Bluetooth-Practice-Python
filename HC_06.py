import json

with open('data.json') as f:
  data = json.loads(f)
  print(data['acc_x'])

