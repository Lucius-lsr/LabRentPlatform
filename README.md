# LabRentPlatform

## API
注册

```
Method: POST

URL:api/v1/register

Body:
{
 'username': '',   
 ‘email’:  '',     // 任何邮箱均可
 'password': ''
}

Response:
{
 '验证已重新发送，请尽快前往您的邮箱激活，否则无法登陆'
}
```

登录

```
Method: Patch

URL:api/v1/login

Body:
{
 'username': '',
 'password': ''
}

Response:
{
 'username': '',
 'isprovider':'',
}
```

登出

```
Method: Patch

URL:api/v1/logout

Response:
{
 message:'ok'
}
```

获取设备列表

```
Method: Get

URL:api/v1/post

QueryParam:
{
 'page':1
 'name':    //空则搜索全部，否则部分匹配
}

Response:
{
"page": 1, 
"total_page": 1, 
"posts": [{"id": 1, "name": "gpu", "description": "123gpu", "count": 10, "provider": "li"}]
}
```

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

获取申请信息列表

```
Method: Get

URL:api/v1/applylist

Response:
{
 posts:[{
     "count": 2, 
     "target_equipment": {
         'id':1, 
         "name": "GPU", 
         "description": "is GPU", 
         "count": 5, 
         "provider":   "1234567890"}, 
     "end_time": "2020-09-07T15:00:00Z", 
     "reason": "i love it", 
     "state": 0}] // (0, 'pending'), (1, 'accept'), (2, 'refuse'), (3, 'returned')
}
```

获取租借成功列表

```
Method: Get

URL:api/v1/borrowlist

Response:
{
     posts:[{
         "count": 2, 
         "target_equipment": {
             'id':1, "name": 
             "GPU", "description": "is GPU", 
             "count": 5, "provider": "1234567890"}, 
             "end_time": "2020-09-07T15:00:00Z"
          }]
}
```

成为设备提供者

```
Method: PUT

URL:api/v1/upgrade

Body:
{
  lab_info:
}

Response:
{
 message:'ok'
}
```

查询设备

```
Method: Get

URL:api/v2/search


QueryParam:
{
 'username': "",(selectable)
 'name': "",(selectable)
 'page': 1, 
}

Response:
{
 'page': ,
 'total_page': ,
 'posts': [
    {
        'id': ,
        'name': ,
        'description': ,
        'count': ,
        'provider': ,
    }
    ]
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

查询己方设备列表

```
Method: GET

URL:api/v2/equipmentlist

QueryParam:
{
 'page': 1,(selectable)
}

Response:
{
 'page': ,
 'total_page': ,
 'posts': [
    {
        'id': ,
        'name': ,
        'description': ,
        'count': ,
        'provider': ,
    }
    ]
}

```


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

增加设备

```
Method: POST

URL:api/v2/add

QueryParam:
{
 ‘id’: 
 'count': 1,(selectable)
}

Response:
{
 'message'：ok
}
```

删除设备

```
Method: DELETE

URL:api/v2/delete

QueryParam:
{
 ‘id’: 
 'count': 1,(selectable)
}

Response:
{
 'message'：ok
}
```

上架设备

```
Method: POST

URL:api/v2/onshelf

QueryParam:
{
 'name': ,
 'description': ,   // 设备描述
 'remarks':   // 上架理由
 'count': 
}

Response:
{
 'message'：ok
}
```

下架设备

```
Method: DELETE

URL:api/v2/offshelf

QueryParam:
{
 'equipment_id':
}

Response:
{
 'message'：ok
}
```

查看所有的租借申请

```
Method: Get

URL:api/v2/borrowapplylist

QueryParam:
{
 'page': 1, (selectable)
}

Response:
{
    'page': ,
    'total_page': ,
    'borrow_apply_list': [{
        'id':1, 
        'borrower': "",
        'count': ,
        'target_equipment': "",
        'endtime': "",
        'reason': "",
        'state': 0 or 1 or 2 or 3
    }]
}
```

是否同意申请

```
Method: PUT

URL:api/v2/whether/agree

QueryParam:
{
 'id':     //BorrowAplly的id
 'flag':   //1同意 2拒绝
}

Response:
{
 'message':ok
}
```

查看所有已借出设备历史信息

```
Method: Get

URL:api/v2/lendlist

Response:
{
"posts":[
{
    "id": 2,
    "borrower": "li",
    "count": 2,
    "target_equipment":{
        "id": 2, 
        "name": "电脑", 
        "description": "123电脑", 
        "count": 10
    },
    "endtime": "2020-09-22T14:51:33Z",
    "reason": "没有理由",
    "state": 3
}
]
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

