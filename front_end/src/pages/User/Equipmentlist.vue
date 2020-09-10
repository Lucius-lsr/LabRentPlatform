<template>
<div>
  <el-table
    ref="multipleTable"
    :data="tableData"
    tooltip-effect="dark"
    style="width: 100%"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
    <el-table-column
      label="设备编号"
      width="120">
      <template slot-scope="scope">{{ scope.row.id }}</template>
    </el-table-column>
    <el-table-column
      prop="name"
      label="设备名称"
      width="120">
    </el-table-column>
    <el-table-column
      prop="description"
      label="设备描述"
      show-overflow-tooltip>
    </el-table-column>
    <el-table-column
      prop="count"
      label="设备数量"
      width="120">
    </el-table-column>
    <el-table-column
      prop="provider"
      label="设备提供者"
      width="120">
    </el-table-column>
  </el-table>
  <div style="margin-top: 100px">
    <el-input v-model="inputname" placeholder="请输入需要检索的设备名称"></el-input>
    <el-button style="margin: 30px 0px 0px 0px" @click="searchName(inputname)">检索</el-button>
    <el-button style="margin: 30px 0px 0px 30px" @click="cancleName()">取消设备名称筛选</el-button>
  </div>
  <div style="margin-top: 20px">
    <el-button @click="prePage()">上一页</el-button>
    <el-button @click="nextPage()">下一页</el-button>
    <el-button @click="toggleSelection()">取消勾选</el-button>
  </div>
</div>
</template>

<script>
  import api from "../../api"

  export default {
    name:"equipmentlist",
    data() {
      return {
        tableData: [],
        multipleSelection: [],
        inputname: '',
        name:'',
        page:1,
        total_page: 0
      }
    },

    mounted(){
      api.getequipmentlist(1,'').then(res =>{
        //console.log(res)
        this.tableData = res.data.posts;
        this.total_page = res.data.total_page;
        // console.log(this.tableData)
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

      searchName(name) {
        this.name = name;
        api.getequipmentlist(1,name).then(res =>{
          this.tableData = res.data.posts;
          this.total_page = res.data.total_page;
        })
      },
      cancleName() {
        this.inputname = '';
        this.name = '';
        api.getequipmentlist(1,'').then(res =>{
          this.tableData = res.data.posts;
          this.total_page = res.data.total_page;
        })
      },

      prePage() {
        if(this.page == 1){
          alert("当前已是第一页")
        }
        else {
          this.page--;
          api.getequipmentlist(this.page,this.name).then(res =>{
            this.tableData = res.posts;
          })
        }
      },
      nextPage() {
        if(this.page == this.total_page){
          alert("当前已是最后一页")
        }
        else {
          this.page++;
          api.getequipmentlist(this.page,this.name).then(res =>{
            this.tableData = res.posts;
          })
        }
      }

    }
  }
</script>