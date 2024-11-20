curl -X PATCH http://0.0.0.0:8000/nomenclature/ \
-H "Content-Type: application/json" \
-d '{
    "group": {
      "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "uuid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    },
    "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "range": {
      "base_unit": null,
      "conversion_factor": 1,
      "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "uuid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    },
    "uuid": "22222222-2222-2222-2222-222222222222"
  }'

curl -X GET http://0.0.0.0:8001/storehouse/get_transaction
