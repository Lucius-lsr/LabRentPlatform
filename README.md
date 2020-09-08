# LabRentPlatform

## API
注册

```
Method: POST

URL:api/v1/register

Request:
{
 'username': '',   // 必须是10位数学号
 ‘email’:  '',     // 只在注册的时候用于验证
 'password': ''
}

Response:
{
 message:'ok'
}
```

登录

```
Method: Patch

URL:api/v1/login

Request:
{
 'username': '',
 'password': ''
}

Response:
{
 'username': '',
 'isprovider':'',
 'jwt': ''
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
 'name':
}

Response:
{
 'page'：1
  posts:[]
}
```

申请租借

```
Method: POST

URL:api/v1/apply

QueryParam:
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
 posts:[{"count": 2, "target_equipment": {"name": "GPU", "description": "is GPU", "count": 5, "provider": "1234567890"}, "end_time": "2020-09-07T15:00:00Z", "reason": "i love it", "state": 0}]
}
```

获取租借成功列表

```
Method: Get

URL:api/v1/rentlist

Response:
{
 posts:[{"count": 2, "target_equipment": {"name": "GPU", "description": "is GPU", "count": 5, "provider": "1234567890"}, "end_time": "2020-09-07T15:00:00Z"}]
}
```

成为设备提供者

```
Method: PUT

URL:api/v1/upgrade

QueryParam:
{
  lab_info:
}

Response:
{
 message:'ok'
}
```

设备提供者新权限

查询设备

```
Method: Get

URL:api/v2/search

Response:
{
 posts:[]  #equipment information
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
 'address':
 'endtime':
 'contact':
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
 'name':
 'address':
 'endtime':
 'contact':
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
 'id':
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
 'id':
 'remarks'://上架时给出的备注消息
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
 'id':
}

Response:
{
 'message'：ok
}
```

查看所有的租借申请

```
Method: Get

URL:api/v2/offshelf

Response:
{
 'posts':[]
}
```

是否同意申请

```
Method: PUT

URL:api/v2/whether/agree

QueryParam:
{
 'id':
 'flag':
}

Response:
{
 'message':ok
}
```

查看所有已借出设备历史信息

```
Method: Get

URL:api/v2/searchrent

Response:
{
 'posts':[]
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


