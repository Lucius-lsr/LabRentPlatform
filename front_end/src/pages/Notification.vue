<template>
  <div>
    <div v-if="messages.length">
      <div v-for="index in (0,messages.length)" :key="index">
        <div style="margin: 5px">
          <el-card class="box-card">
            <div slot="header">
                <span
                  v-if="messages[index-1]"
                  width="30%"
                  style="float: left"
                >type:  {{messages[index-1].type}}</span>

                <span v-if="messages[index-1]">
                  state:{{state(messages[index-1].state)}}
              </span>
            </div>
             <div class="text item"  v-if="messages[index-1]" v-html="messages[index-1].apply.target_equipment"></div><br/>
            <div class="text item" v-if="messages[index-1]">备注：{{messages[index-1].apply.remarks}}</div>
          </el-card>
        </div>
      </div>
    </div>

    
    
    
  </div>
</template>

<script>
import api from "../api";

export default {
  name: "Notification",
  data() {
    return {
      messages: []
    }
  },
  mounted(){
    api.notice().then((res) => {
      this.messages = res.data.notification;

    //   console.log(this.messages[0].apply)
    //    console.log( res.data)
    })
  },
  methods: {
      state(state)
      {
          if(state==1)return'成功'
          if(state==2)return'拒绝'
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