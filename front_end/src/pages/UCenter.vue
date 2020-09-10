<template>
    <div>  
        <div style="margin: 5px"> 
        <el-card >
        <div slot="header">
        <span v-if="info" >
            <span style="float: left;padding: 0px 0px 0px 100px">个人信息</span>
        </span>
        </div>
        <div style="float:left">
           你好，用户{{username}}!
        </div><br /><br /><br />
        
        
        <el-button style="float:left ; margin: 30px 30px 30px 0px" type="primary" @click="up_apply()">申请成为设备提供者</el-button>
        <el-button style="margin: 30px 30px 0px 0px" type="primary" @click="logout()">登出</el-button><br />
        <el-input style="min-height:200px" type="textarea" :autosize="{ minRows: 5 , maxRows:10}"  placeholder="请输入申请成为设备提供者的原因"  v-model="textarea"></el-input>
        </el-card>
        </div>
    </div>
</template>

<script>
import api from "../api"
export default {
    name:"Ucenter",
    data()
    {
        return{
            info:"",
            textarea:"",
            username:""
        }
    },
    mounted(){
        this.username=localStorage.getItem("username")
    },
    methods:{
        logout(){
            api.getLogout().then(res =>{
            // console.log(res)
            if(res.status==200){
            this.$message('成功登出')
            localStorage.setItem("token","")
            this.$router.push('/login')
            }
            })
        
            
        },
        up_apply(){
            if(this.textarea=='')
            {
                this.$message({
                                    showClose: true,
                                    message: "申请理由不能为空！",
                                    type: "error"
                            })
                return
            }

            api.upgrade_apply(
                {
                    "lab_info":this.textarea
                }
            ).then(res =>{
            // console.log(res)
            if(res.status==200){
             this.$message('您的申请已成功发送！')
            }
            })
        }
    }
    
}
</script>