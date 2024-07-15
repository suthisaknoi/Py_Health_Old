import json

data = {
  "pid": "3650600299197",
  "titleName": "003",
  "fname": "สุทธิศักดิ์",
  "lname": "เปรมเกิด",
  "nation": "099",
  "birthDate": "25130210",
  "sex": "ชาย",
  "transDate": "2022-03-04T00:00:00",
  "mainInscl": "(OFC) สิทธิข้าราชการ/สิทธิหน่วยงานรัฐ",
  "subInscl": "(O3) สิทธิเบิกกรมบัญชีกลาง (ผู้รับเบี้ยหวัดบำนาญ)",
  "age": "54 ปี 4 เดือน 22 วัน",
  "checkDate": "2024-07-02T05:39:27",
  "claimTypes": [
    {
      "claimType": "PG0060001",
      "claimTypeName": "เข้ารับบริการรักษาทั่วไป (OPD/ IPD/ PP)"
    },
    {
      "claimType": "PG0110001",
      "claimTypeName": "Self Isolation"
    },
    {
      "claimType": "PG0120001",
      "claimTypeName": "UCEP PLUS (ผู้ป่วยกลุ่มอาการสีเหลืองและสีแดง)"
    },
    {
      "claimType": "PG0130001",
      "claimTypeName": "บริการฟอกเลือดด้วยเครื่องไตเทียม (HD)"
    }
  ],
  "correlationId": "0de4aafc-e62a-482c-a86e-7ff6b80e7885",
  "startDateTime": "2022-03-04T00:00:00"
}


list1 = json.loads(data)
print(list1)


