1.注册

```
Method: POST

URL:api/v1/register

Request:
{
 'username': '',
 'password': ''
}

Response:
{
 message:'ok'
}
```

2.登录

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

3.登出

```
Method: Patch

URL:api/v1/logout

Response:
{
 message:'ok'
}
```

4.获取设备列表

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

5.申请租借

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

6.获取申请信息列表

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

7.获取租借成功列表

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

8.成为设备提供者

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

9.查询设备

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

10.修改己方设备信息

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

11.增加设备

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

12.删除设备

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

13.上架设备

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

14.下架设备

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

15.查看所有的租借申请

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

16.是否同意申请

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

17.查看所有已借出设备历史信息

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

18.确认归还

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

