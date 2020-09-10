/**
 * 网络请求：Axios
 */

import axios from "axios"
import router from "../router"
// import store from "../store"

// 错误信息的响应方法
const errorHandle = (status,other) => {
    switch(status){
        case 400:
            // 请求头和服务器的限制
            //console.log(" 服务器不理解请求的语法");
            this.alert('错误400，服务器不理解请求的语法！')
            // toLogin();
            router.push("/400")
            break;
    //     case 401:
    //         // token验证失败，用户身份验证失败
    //         //console.log("（未授权）请求要求身份验证");
    //         // this.$message('错误401，（未授权）请求要求身份验证')
    //         // toLogin();
    //         router.push("/401")
    //         break;
        case 403:
            // 用户身份过期了，服务器请求限制
            //console.log("（禁止） 服务器拒绝请求");
            this.$message('错误403，权限错误')
            // toLogin();
            break;
        case 404:
            // 网络请求地址错误
            // console.log("（未找到） 服务器找不到请求的网页。");
            // this.$message('错误404，（未找到） 服务器找不到请求的网页')
            router.push("/404")
            break;
        default:
            console.log(other);
            break;
            
    }
}

// 创建axios对象
const instance = axios.create({
    timeout:5000  // 请求超时
})

// 创建请求拦截和响应拦截操作
instance.interceptors.request.use(config =>{
        // 判断token是否存在，存在则携带，通过请求头
        const token = localStorage.getItem("token");
        // console.log(token)
        if(token){
            config.headers.session_id = token;
        }
        return config;
    },
    error => Promise.reject(error)
)

instance.interceptors.response.use(
    
    response => response.status === 200 ? Promise.resolve(response) : Promise.reject(response),
    
    error => {
        const { response } = error; 
        /**
         * response包含的信息：
         *  status
         *  data
         */
        if(response){
            // 给出开发者具体的错误信息
            errorHandle(response.status,response.data);
            return Promise.reject(response);
        }else{
            console.log("请求中断或者断网了");
        }
    }
)

export default instance;