<template>
  <div>
    <div v-if="messages">
      <div v-for="index in (0,messages.length)" :key="index">
        <div style="margin: 5px">
          <el-card class="box-card">
            <div slot="header">
              <span>
                <span
                  v-if="messages[index-1]"
                  width="30%"
                  style="float: left"
                >id:{{messages[index-1].id}}</span>
                <span>
                  发送者：{{messages[index-1].sender}}
                  <span class="bank"></span>
                  接收者：{{messages[index-1].receiver}}
                </span>
                <span v-if="messages[index-1].is_read" class="bank">已读</span>
                <span v-if="!messages[index-1].is_read" class="bank">未读</span>
                
              </span>
            </div>
            <div class="text item" v-html="messages[index-1].content"></div>
          </el-card>
        </div>
      </div>
    </div>

    <el-row :gutter="10">
        <el-col :span="3"><el-button
        type="primary"
        icon="el-icon-edit"
        style="float: left;margin: 20px 0 20px 0"
        @click="send()"
        >发送消息</el-button></el-col>
        <el-col :span="3"><el-button
        type="primary"
        icon="el-icon-edit"
        style="margin: 20px 0px 20px 0"
        @click="readall()"
        >一键已读</el-button></el-col>
    </el-row>
    <el-input type="textarea" autosize placeholder="请输入接收人名" v-model="textarea1"></el-input>
    <div style="margin: 20px 0"></div>
    <el-input
      style="max-height:100px"
      type="textarea"
      :autosize="{ minRows: 2 , maxRows:10}"
      placeholder="请输入消息内容"
      v-model="textarea2"
    ></el-input>
  </div>
</template>

<script>
import api from "../api";

export default {
  name: "Messagelist",
  data() {
    return {
      messages: "",
      textarea1: "",
      textarea2: "",
    };
  },
  mounted() {
    api.getmessages().then((res) => {
      this.messages = res.data.messages;
      // console.log(this.messages)
      // console.log(this.messages.length)
    });
  },
  methods: {
    send() {
      if (this.textarea1 == "" || this.textarea2 == "") {
        this.$message("内容不能为空！");
        return;
      }
      let params = {
        "receiver_name": this.textarea1,
        "content": this.textarea2,
      };
      api
        .sendmessage(params)
        .then((res) => {
        //   console.log(res);
          if (res.status == 200) {
            this.$message("发送消息成功！");
          }
        })
        .catch((error) => {
          if (error.data["error"]) {
            this.$message({
              showClose: true,
              message: error.data["error"],
              type: "error",
            });
          }
        });
    },

    readall(){
        api.readmessages().then((res) => {
        //   console.log(res);
          if (res.status == 200) {
            this.$message("成功一键已读！");
            //重新渲染
            api.getmessages().then((res) => {
                this.messages = res.data.messages;
                    // console.log(this.messages)
            // console.log(this.messages.length)
            });
          }
        })
        .catch((error) => {
          if (error.data["error"]) {
            this.$message({
              showClose: true,
              message: error.data["error"],
              type: "error",
            });
          }
        });
    }
  },
};
</script>
<style>
.bank {
  padding-left: 1.8em;
}
.text {
  font-size: 14px;
}

.item {
  font-size: 13px;
  float: left;
}

.box-card {
  width: 100%;
}
</style>