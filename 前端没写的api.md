# LabRentPlatform

## API


申请租借

```
Method: POST

URL:api/v1/apply

Body:
{
 'id':
 'endtime':
 ’reason':
 'count':  //借多少个
}

Response:
{
 message:'ok'
}
```



发送消息
```
Method: POST
URL:api/v1/sendmessage
QueryParam:
{
 'receiver_id':,
 'content':
}
Response:
{
 'message'：ok
}
```

获得消息
```
Method: GET
URL:api/v1/getmessages
QueryParam:
{
 'receiver_id':,
 'content':
}
Response:
{
    "total": 2,
    "new_message": 2,
    "messages": [
        {
            "id": 1,
            "sender": "2017011672",
            "receiver": "2017011672",
            "content": "this is content",
            "is_read": false
        },
        {
            "id": 2,
            "sender": "2017011672",
            "receiver": "2017011672",
            "content": "content",
            "is_read": false
        }
    ]
}
```

阅读消息
```
Method: PUT
URL:api/v1/readmessages
Response:
{
 'message'：ok
}
```

## 设备提供者新权限



修改己方设备信息

```
Method: PUT

URL:api/v2/edit

QueryParam:
{
 'id':
 'name':
 'description':
 'count':
}

Response:
{
 'message'：ok
}
```




确认归还

```
Method: PUT

URL:api/v2/confirm

QueryParam:
{
 'id':
}

Response:
{
 'message':ok
}
```


获取通知

```
Method: GET

URL:api/v1/notification

Response:
{
 notifications:[
     {
         'type':'borrow apply',  // 或upgrade apply或onshelf apply
         'state': 1,     // 1 accept, 2 refuse
         'apply':  // 通知对象的具体信息，可以是租借申请/升级申请/上架申请
         {
                'id':1, 
                'borrower': "",
                'count': ,
                'target_equipment': "",
                'endtime': "",
                'reason': "",
                'state': 0 or 1 or 2 or 3
         }
     }
 ]
}
```

