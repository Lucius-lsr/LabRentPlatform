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
 'username':
 'id':
 'endtime':
 ’reason':
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

QueryParam:
{
 'username':1
}

Response:
{
 posts:[]
}
```

获取租借成功列表

```
Method: Get

URL:api/v1/rentlist

QueryParam:
{
 'username':1
}

Response:
{
 posts:[]
}
```

成为设备提供者

```
Method: PUT

URL:api/v1/upgrade

QueryParam:
{
 'username':1
  manythings to add
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

QueryParam:
{
 'username':1
}

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
  #'username':1 可以不加，不验证这个设备是否属于这个用户
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
 'username':
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
 'username':
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

QueryParam:
{
 'username':
}

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

QueryParam:
{
 'username'
}

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


