<template>
    <div class="details">
        <div class = "myborder">
            <el-row style="margin-top: 20px;margin-left: 20px;">ID：{{id}}</el-row>
            <el-row style="margin-top: 20px;margin-left: 20px;">设备名：{{name}}</el-row>
            <el-row style="margin-top: 20px;margin-left: 20px;">设备数目：{{count}}</el-row>
            <el-row style="margin-top: 20px;margin-left: 20px;">设备提供者：{{provider}}</el-row>
            <el-row style="margin-top: 20px;margin-left: 20px;">设备描述：</el-row>
            <el-row style="margin-top: 20px;margin-left: 40px;margin-bottom: 20px;">{{description}}</el-row>
        </div>
        <el-row :gutter="5" style="margin-top: 40px;">
            <el-col :span="2"><el-button type="primary" @click="modify()">修改信息</el-button></el-col>
            <el-col :span="2"><el-button type="success" @click="add()">增加设备</el-button></el-col>
            <el-col :span="4"><el-input placeholder="数目（正整数）" v-model="num"  @blur="number($event)"></el-input></el-col>
            <el-col :span="2"><el-button type="danger"  @click="minus()">减少设备</el-button></el-col>
        </el-row>

   <el-dialog
      title="修改信息"
      :visible.sync="modifyVisible"
      :before-close="handleClose"
      style="font-size: 30px;"
    >
      <div class="info" :model="modifyContent">
        <el-row ><span class="lable">ID:</span></el-row >
        <div style="margin: 10px 0;"></div>
        <el-row ><span class="lable" style="margin-left: 10px;">{{id}}</span></el-row >
        <!-- <el-row >id：{{id}}</el-row> -->
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备名称：</span>
        <el-input
          placeholder="请输入设备名称"
          clearable
          v-model="modifyContent.name"
        >
        </el-input>
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备数目：</span>
        <el-input
          placeholder="请输入设备数目"
          clearable
          v-model="modifyContent.count"
        >
        </el-input>
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备提供者：</span>
        <div style="margin: 10px 0;"></div>
         <el-row ><span class="lable" style="margin-left: 10px">{{provider}}</span></el-row >
                <!-- <el-row>设备提供者：{{provider}}</el-row> -->
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备描述：</span>
        <div style="margin: 20px 0;"></div>
        <el-input
          type="textarea"
          :autosize="{ minRows: 6, maxRows: 10 }"
          placeholder="请输入内容"
          clearable
          v-model="modifyContent.description"
        >
        </el-input>

        <el-button
          type="primary"
          style="margin : 4% 90%"
          @click="submitMyModify()"
          >提交</el-button
        >
      </div>
    </el-dialog>
    </div>
</template>

<script>
import api from "../../../api/index.js"
import router from "../../../router/index.js"

export default {
    data(){
        return{
            id: this.$route.params.id,
            name: this.$route.params.name,
            count: this.$route.params.count,
            description: this.$route.params.description,
            provider: this.$route.params.provider,
            num: 0,
            modifyVisible: false,
            modifyContent: {
                // id: this.id,
                name: this.name,
                count: this.count,
                description: this.description,
                // provider: this.provider
            },
        }
    },
    methods:{
        modify(){
                // this.modifyContent.id = this.id,
                this.modifyContent.name = this.name,
                this.modifyContent.count = this.count,
                this.modifyContent.description = this.description,
                this.modifyVisible = true
        },
        submitMyModify(){
            if(!this.modifyContent.name || !this.modifyContent.count ||! this.modifyContent.description){
                this.$message({
                    showClose: true,
                    message: "输入不能为空",
                    type: "error"
                });
            }else{
                let params = {
                    id:this.id,
                    name:this.name,
                    description: this.description,
                    count: this.count
                }
                api.modifyEquipment(params)
                .then(res =>{
                    this.$message({
                        showClose: true,
                        message: res.data["message"] + ",修改成功",
                        type: "success"
                    });

                    this.modifyVisible = false;
                    // this.showPostDetails();
                    this.returnList();
                })
                .catch(error => {
                    if (error.response) {
                        //返回错误code
                        this.$message({
                        showClose: true,
                        message: error.response.data.message,
                        type: "error"
                        });
                    }else{
                        this.$message({
                            showClose: true,
                            message: error.data['error'],
                            type: "error"
                        });
                    }
                });
            }
        },
        number(e) {
            console.log(e.target.value);
            let flag = new RegExp("^[1-9]([0-9])*$").test(e.target.value);
            // console.log(flag);
            if (!flag) {
                this.$message({
                    showClose: true,
                    message: "请输入正整数",
                    type: "warning"
                });
            }
        },
        add(){
            let flag = new RegExp("^[1-9]([0-9])*$").test(this.num);
            if (!flag) {
                this.$message({
                    showClose: true,
                    message: "请输入正整数",
                    type: "error"
                });
            }else{
                let params = {
                    id: this.id,
                    count: this.num
                }
                api.addEquipment(params)
                .then(res =>{
                    this.$message({
                        showClose: true,
                        message: res.data["message"] + ",增加成功",
                        type: "success"
                    });
                    // this.showPostDetails();
                    this.returnList();
                })
                .catch(error => {
                    if (error.response) {
                        //返回错误code
                        this.$message({
                        showClose: true,
                        message: error.response.data.message,
                        type: "error"
                        });
                    }else{
                        this.$message({
                            showClose: true,
                            message: error.data['error'],
                            type: "error"
                        });
                    }
                });
            }
        },
        minus(){
            let flag = new RegExp("^[1-9]([0-9])*$").test(this.num);
            if (!flag) {
                this.$message({
                    showClose: true,
                    message: "请输入正整数",
                    type: "error"
                });
            }else{
                if(Number(this.num) > Number(this.count)){
                    this.$message({
                        showClose: true,
                        message: "设备数目不足，无法减少",
                        type: "error"
                    });
                    return;
                }
                let params = {
                    id: this.id,
                    count: this.num
                }
                api.minusEquipment(params)
                .then(res =>{
                    this.$message({
                        showClose: true,
                        message: res.data["message"] + ",减少成功",
                        type: "success"
                    });
                    // this.showPostDetails();
                    this.returnList();
                })
                .catch(error => {
                    if (error.response) {
                        //返回错误code
                        this.$message({
                        showClose: true,
                        message: error.response.data.message,
                        type: "error"
                        });
                    }else{
                        this.$message({
                            showClose: true,
                            message: error.data['error'],
                            type: "error"
                        });
                    }
                });
            }
        },
        returnList(){
            router.push({
                name: "MyEquipmentList",
            });
        },
        handleClose(done) {
            this.$confirm("确认放弃更改？")
            .then(_ => {
                done();
                console.log(_);
            })
            .catch(_ => {
                console.log(_);
            });
        },

    }
}
</script>
<style scoped>
.details{
    text-align: left;
}
.myborder{
    border-color: teal;
    border-style: dashed;
    font-size: 18px;
}
.lable{
    margin-top: 10px;
}
</style>