

<template>
<div>
  <el-table
    ref="multipleTable"
    :data="tableData"
    :row-class-name="tableRowClassName"
    tooltip-effect="dark"
    style="width: 100%"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
    <el-table-column
      label="申请数量"
      width="60">
      <template slot-scope="scope">{{ scope.row.count }}</template>
    </el-table-column>
    <el-table-column
      label="设备编号"
      width="60">
      <template slot-scope="scope">{{ scope.row.target_equipment.id }}</template>
    </el-table-column>
    <el-table-column
      label="设备名称"
      width="120">
      <template slot-scope="scope">{{ scope.row.target_equipment.name }}</template>
    </el-table-column><el-table-column
      label="设备描述"
      width="120">
      <template slot-scope="scope">{{ scope.row.target_equipment.description }}</template>
    </el-table-column><el-table-column
      label="设备数量"
      width="60">
      <template slot-scope="scope">{{ scope.row.target_equipment.count }}</template>
    </el-table-column>
    <el-table-column
      label="设备提供者"
      width="120">
      <template slot-scope="scope">{{ scope.row.target_equipment.provider }}</template>
    </el-table-column>
    <el-table-column
      label="归还时间"
      width="120">
      <template slot-scope="scope">{{ scope.row.end_time }}</template>
    </el-table-column>
    <el-table-column
      label="申请原因"
      width="120">
      <template slot-scope="scope">{{ scope.row.reason }}</template>
    </el-table-column>
    <el-table-column
      label="申请状态"
      width="120">
      <template slot-scope="scope">{{ state(scope.row.state) }}</template>
    </el-table-column>
  </el-table>

  <div style="margin-top: 20px">
    <el-button @click="toggleSelection()">取消勾选</el-button>
  </div>
</div>
</template>

<script>
  import api from "../../api"

  export default {
    name:"applylist",
    data() {
      return {
        tableData: [],
        multipleSelection: [],
      }
    },

    mounted(){
      api.getapplylist().then(res =>{
        this.tableData = res.posts;
      })
    },

    methods: {
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      tableRowClassName({row, rowIndex}) {
        console.log(rowIndex)
        if (row.state === 0) {
          return 'pending-row';
        } else if (row.state === 1) {
          return 'success-row';
        }
        else if (row.state === 2) {
          return 'reject-row';
        }
        return 'done-row';
        
      },

      state(state) {
        if(state==0){return '申请中'}
        else if(state==1){return '通过申请'}
        else if(state==2){return '拒绝申请'}
        else if(state==3){return '已归还'}
      }
    }
  }
</script>

<style>
  .el-table .pending-row {
    background: #E6A23C;
  }

  .el-table .success-row {
    background: #67C23A;
  }

  .el-table .reject-row {
    background: #F56C6C;
  }

  .el-table .done-row {
    background: #909399;
  }
</style>