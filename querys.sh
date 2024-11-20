curl -X PATCH http://0.0.0.0:8000/nomenclature/ -H "Content-Type: application/json" -d \
'{
  "group": {
      "name": "АААААААААААААА",
      "uuid": "46e30a50-706c-4019-929b-0116321451db"
  },
  "name": "Пшеничная мука",
  "range": {
      "base_unit": null,
      "conversion_factor": 1,
      "name": "грамм",
      "uuid": "46e30a50-706c-4019-929b-0116321451db"
  },
  "uuid": "22222222-2222-2222-2222-222222222222"
}'
curl -X GET http://0.0.0.0:8001/storehouse/get_transaction
