<template>
  <div class="lendlist">
    <el-table
      :data="tableData"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="申请ID" width="150"> </el-table-column>
      <el-table-column prop="target_equipment.name" label="设备名称" ></el-table-column>
      <el-table-column prop="count" label="设备数目" width="150"></el-table-column>
      <el-table-column prop="endtime" label="归还时间" width="200"></el-table-column>      
      <el-table-column prop="borrower" label="申请人" width="150"></el-table-column>
      <el-table-column prop="state" label="状态" width="150">
        <template slot-scope="scope">
            <div v-if="scope.row.state === 1" style="color=green">已租借</div>
            <div v-if="scope.row.state === 3" style="color=rgb(132, 43, 226)">已归还</div>
        </template></el-table-column>
      <el-table-column label="操作" width="200">
          <template slot-scope="scope">
        <el-button
          type="primary"
          @click="handleDetails(scope.$index)">详情</el-button>
        <el-button
          type="success"
          v-if="scope.row.state === 1"
          @click="handleReturn(scope.row)">确认归还</el-button>
      </template></el-table-column>
      
    </el-table>


    <div v-if="tableData[0]">
    <el-dialog
      title="租借申请"
      :visible.sync="dialogVisible"
      style="font-size: 30px;"
    >
     
      <el-row class="info">申请ID: {{ tableData[currentIndex].id }}</el-row>
      <el-row class="info">设备:</el-row>
      <el-row class="info"><el-col :offset="2">ID: {{ tableData[currentIndex].target_equipment.id }}</el-col></el-row>
      <el-row class="info"><el-col :offset="2">名称: {{ tableData[currentIndex].target_equipment.name }}</el-col></el-row>
      <el-row class="info"><el-col :offset="2">总数: {{ tableData[currentIndex].target_equipment.count }}</el-col></el-row>
      <el-row class="info"><el-col :offset="2">描述: {{ tableData[currentIndex].target_equipment.description }}</el-col></el-row>
      <el-row class="info">申请租借数目: {{ tableData[currentIndex].count }}</el-row>
      <el-row class="info">归还时间: {{ tableData[currentIndex].endtime }}</el-row>
      <el-row class="info">申请人: {{ tableData[currentIndex].borrower }}</el-row>
      <el-row class="info">申请状态：
          <el-col :offset="2" v-if="tableData[currentIndex].state=== 1" style="color=green">已租借</el-col>
          <el-col :offset="2" v-if="tableData[currentIndex].state=== 3" style="color=rgb(132, 43, 226)">已归还</el-col>
      </el-row>
      <el-row class="info">申请原因：</el-row>
      <el-row class="info">
          <el-col :offset="2">{{tableData[currentIndex].reason}}</el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确定</el-button>
      </span>
    </el-dialog>
    </div>
  </div>
</template>

<script>

import api from "../../../api/index"

export default {
  name: "LendList",
  data(){
    return{
      tableData:[],
      dialogVisible: false,
      currentIndex: 0
    }
  },
  mounted(){
    this.getList();       
  },
  methods:{
      getList(){
        api.getLendList()
        .then(res =>{
          this.tableData = res.data.posts;
        })
        .catch(error => {
            this.$message({
              showClose: true,
              message: error.data['error'],
              type: "error"
            });
        })
      },
    handleDetails(index) {
        this.currentIndex = index;
        this.dialogVisible = true;
      },
    handleReturn(row){
      let pramas = {
        id: row.id
      }
      api.confirmReturn(pramas)
      .then(res =>{
        this.$message({
            showClose: true,
            message: res.data.message + "已确认",
            type: "success"
        });
        this.getList();
      })
      .catch(error => {
        this.$message({
          showClose: true,
          message: error.data['error'],
          type: "error"
        });
      })
    }
    
    },
};
</script>

<style lang="scss" scoped>
.info {
  text-align: left;
  font-size: 20px;
  margin-top: 10px;
}
</style>
