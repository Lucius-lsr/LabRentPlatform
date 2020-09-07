# LabRentPlatform

## API

### 普通用户

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

根据用户名`username`或设备名称`name`查找设备
```
Method: GET
URL:api/v1/post
QueryParam:
{
 'page':1
 'name': "",
 'username': "",
 'page': 1
}
Response:
{
 'page'： 1,
 'total_page': 1
  posts: []
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
 posts:[]
}
```

获取租借成功列表

```
Method: Get

URL:api/v1/rentlist

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
  manythings to add
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
 'page': 1，
 ‘username’: "",
 'name': ""
}
Response:
{
 'page'： 1,
 'total_page': 1
  posts: []
}
```

### 设备提供者新权限

查看自己的设备列表
```
Method: GET
URL:api/v2/post
QueryParam:
{
 'page': 1 (selectable)
}
Response:
{
 'page'： 1,
 'total_page': 1
  posts: []
}
```

修改设备信息
```
Method: GET
URL:api/v2/edit
QueryParam:
{
 'name': "", (selectable)
 'username': "", (selectable)
 'page': 1 (selectable)
}
Response:
{
 'page'： 1,
 'total_page': 1
  posts: []
}
```

增加设备数量

```
Method: POST

URL:api/v2/increase

QueryParam:
{
 'id': ,
 'count': 1,  (selectable)
}

Response:
{
 'message'：ok
}
```

减少设备数量

```
Method: POST

URL:api/v2/decrease

QueryParam:
{
 'id': ,
 'count': 1,  (selectable)
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
 'name':
 'description':
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


