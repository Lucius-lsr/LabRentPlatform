/**
 * 网络请求：Axios
 */

import axios from "axios"
import router from "../router"
// import store from "../store"

//错误信息的响应方法
const errorHandle = (status,other) => {
    switch(status){
        case 401:
            // token验证失败，用户身份验证失败
            // this.$message('错误401，（未授权）请求要求身份验证')
            // toLogin();
            router.push("/login")
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
            this.$message("请求中断或者断网了");
        }
    }
)

export default instance;