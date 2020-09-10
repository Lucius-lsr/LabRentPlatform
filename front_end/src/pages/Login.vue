<template>
    <div class="login">
        <h1 class="title">设备租赁智能管理平台</h1>
        <div style="margin-top: 50px"></div>
        <el-row>
            <el-col :span="10" :offset= "3"><el-button class="Menu" @click="changeType('login')">登陆</el-button></el-col>
            <el-col :span="11"><el-button class="Menu" @click="changeType('register')" style="margin-left = 20px">注册</el-button></el-col>
        </el-row>
        <el-form
            :model="ruleForm"
            status-icon
            ref="ruleForm"
            label-width="100px"
            class="demo-ruleForm"
            style="margin-top = 50px"
        >
            <el-form-item label="用户名" prop="username" >
                <el-input type="username" v-model="ruleForm.username" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password" >
                <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email" v-show="type === 'register'">
                <el-input type="email" v-model="ruleForm.email" autocomplete="on"></el-input>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')">{{typeName[type]}}</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
                <el-button @click="logout()">登出</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>

import api from "../api"
import { mapMutations } from "vuex"
// import store from "../store/index.js"

export default {
    name: "Login",
    data() {
        return {
            ruleForm: {
                username: "",
                password: "",
                email:""
            },
            type:"login",
            typeName:{
                "login":"登陆",
                "register":"注册"
            }
        };
    },
    methods: {        
        ...mapMutations("LoginModule",["setToken"]),
        submitForm(formName) {
            // console.log(this.ruleForm)
            if (!this.ruleForm.username || !this.ruleForm.password) { //检测账号密码
                this.$message({
                    showClose: true,
                    message: "账号或密码不能为空",
                    type: "error"
                });
                return;
            }
            if(this.type==="login"){                            //登陆
                this.$refs[formName].validate(valid => {
                    if (valid) {
                        api.getLogin({
                            username:this.ruleForm.username,
                            password:this.ruleForm.password
                        })
                        .then(res =>{
                            if(res.status===200){
                            // console.log(document.cookie);
                            let cookie=String(document.cookie)
                            let index=cookie.indexOf('=')
                            let session_id=cookie.substring(index+1)
                            // console.log(session_id);

                            localStorage.setItem("token",session_id);
                            //this.$router.replace("/");
                            // this.setToken(session_id);

                            localStorage.setItem("username",res.data.user);
                            // //将用户id存下
                            // mydata.mydata.id=res.data.userId
                            console.log(res.data.isprovider);
                            if(res.data.isprovider){
                                localStorage.setItem("isProvider",res.data.isprovider);
                                // this.$store.commit("setRole", res.data.isprovider);
                                
                            }
                            this.$message({
                                showClose: true,
                                message: "登陆成功，欢迎" + res.data.user,
                                type: "success"
                            })
                            this.$router.push('/')
                            }
                        })
                        .catch(error => {
                            // console.log("fail")
                            // console.log(error)
                            if(error.data['error']){
                                this.$message({
                                    showClose: true,
                                    message: error.data['error'],
                                    type: "error"
                            })
                            }
                           
                            
                        })
                    }
                    else {
                        // console.log("error submit!!");
                        return false;
                    }
                })
            }
            //注册
            else{                          
                if (!this.ruleForm.email) {
                    this.$message({
                        showClose: true,
                        message: "邮箱不能为空",
                        type: "error"
                    });
                    return;
                }
                if (!this.ruleForm.username || !this.ruleForm.password) { //检测账号密码
                this.$message({
                    showClose: true,
                    message: "账号或密码不能为空",
                    type: "error"
                });
                return;
                }
                api.getRegister({
                            username:this.ruleForm.username,
                            email:this.ruleForm.email,
                            password:this.ruleForm.password

                        })
                        .then(res =>{
                            // console.log("ok")
                            if(res.status===200){
                                this.$message({
                                    showClose: true,
                                    message: res.data,
                                    type: "success"
                            });
                            }
                        })
                        .catch(error => {
                            // console.log("fail")
                            if (error.response) {
                                //返回错误code
                                // console.log(error.response)
                                this.$message({
                                    showClose: true,
                                    message: error.response.data,
                                    type: "error"
                                });
                            }else{
                                this.$message({
                                    showClose: true,
                                    message: error.data['error'],
                                    type: "error"
                                });
                            }
                        })
            }
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        changeType(type) {
            this.type = type
        },
        logout(){
            api.getLogout().then(res =>{
            // console.log(res)
            if(res.status==200){
            this.$message('成功登出')
            localStorage.setItem("token","")
            }
            })
        }
    }
};
</script>
<style scoped>
.title{
    text-align: center;
}

.login{
    width:800px;
    margin: 0 auto;
    margin-top: 80px;
}
.Menu{
    width: 340px;
}

</style>