<template>
  <div class="borrowapplylist">
    <el-row>
      <el-col :offset="0" :span="2"><el-button type="success" @click="onShelfApply()">上架申请</el-button></el-col>
    </el-row>
    <div style="margin-top: 10px"></div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="设备id" width="150"> </el-table-column>
      <el-table-column prop="name" label="设备名称" ></el-table-column>
      <el-table-column prop="count" label="设备数目" width="150"></el-table-column>
      <el-table-column prop="state" label="上架状态" width="150">
        <template slot-scope="scope">
          <div v-if="scope.row.state === 0" style="color:rgb(105, 105, 105)">等待确认</div>
          <div v-if="scope.row.state === 1" style="color:rgb(132, 43, 226)">已上架</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template slot-scope="scope">
          <el-button
            type="primary"
            @click="handleEdit(scope.$index, scope.row)">详情</el-button>
          <el-button
            type="danger"
            v-if="scope.row.state === 1 "
            @click="handleoffshelf(scope.$index, scope.row)">下架</el-button>
        </template>
      </el-table-column>
      
    </el-table>
    
    <el-footer
      ><layoutFooter
        :totalPage="totalPage"
        @changePage="changePage"
      ></layoutFooter
    ></el-footer>

    <el-dialog
      title="上架申请"
      :visible.sync="applyVisible"
      :before-close="handleClose"
      style="font-size: 30px;"
    >
      <div class="info" :model="applyContent">
        <span class="lable">设备名称：</span>
        <el-input
          placeholder="请输入设备名称"
          clearable
          v-model="applyContent.name"
        >
        </el-input>
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备数目：</span>
        <el-input
          placeholder="请输入设备数目"
          clearable
          v-model="applyContent.count"
        >
        </el-input>
        <div style="margin: 20px 0;"></div>
        <span class="lable">设备描述：</span>
        <div style="margin: 20px 0;"></div>
        <el-input
          type="textarea"
          :autosize="{ minRows: 6, maxRows: 10 }"
          placeholder="请输入内容"
          clearable
          v-model="applyContent.description"
        >
        </el-input>
        <div style="margin: 20px 0;"></div>
        <span class="lable">上架理由：</span>
        <div style="margin: 20px 0;"></div>
        <el-input
          type="textarea"
          :autosize="{ minRows: 6, maxRows: 10 }"
          placeholder="请输入内容"
          clearable
          v-model="applyContent.remarks"
        >
        </el-input>
        <el-button
          type="primary"
          style="margin : 4% 90%"
          @click="submitApply()"
          >提交</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import layoutFooter from "../../../components/LayoutFooter.vue";
import api from "../../../api/index"
import router from "../../../router/index.js"
// import params from "../../../api/index"
export default {
  name: "MyEquipmentList",
  components: {
    layoutFooter
  },
  data(){
    return{
      tableData:[],
      totalPage: 0,
      page: 1,
      applyContent:{
        name: "",
        count: 0,
        description: "",
        remarks: ""
      },
      applyVisible: false
    }
  },
  mounted(){
    this.getList();
  },
  methods:{
      getList(){
        let params = {
          page: this.page
        };
        this.loadList(params);
      },
      loadList(params){
        api.getMyEquipmentList(params)
        .then(res =>{
          this.page = res.data.page;
          this.totalPage = res.data.total_page;
          this.tableData = res.data.posts;
        })
        .catch(error => {
            this.$message({
              showClose: true,
              message: error.data['error'],
              type: "error"
            });
        });
      },
      
      changePage(page) {
        this.page = page;
        this.search();
      },
      handleEdit(index, row) {
        console.log(index, row);
        router.push({
          name: "MyEquipmentDetails",
          params: {
            id: row.id,
            name: row.name,
            count: row.count,
            description: row.description,
            provider: row.provider, 
          }
        });
      },
      handleoffshelf(index, row){
        console.log(index, row);
        let params = {
          equipment_id: row.id
        }
        api.offShelf(params)
        .then(res =>{
            this.$message({
              showClose: true,
              message: res.data["message"] + ",下架成功",
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
        });
      },
      search(){
        let params = {
          page: this.page,
          name: this.searchName
        };
        this.loadList(params); 
      },
      onShelfApply() {
        this.applyVisible = true;
      },
      submitApply() {
        if(!this.applyContent.name || !this.applyContent.description || !this.applyContent.remarks || this.applyContent.count){
          let params = {
            name: this.applyContent.name,
            description: this.applyContent.description,
            remarks: this.applyContent.remarks,
            count: this.applyContent.count,
          }
          api.onShelfApply(params)
          .then(res =>{
            if(res.status == 200){
              this.$message({
                showClose: true,
                message: res.data["message"] + ",上架申请已发送，请等待管理员确认",
                type: "success"
              });
              this.getList();
              this.applyVisible = false;
            }
          })
          .catch(error => {
            this.$message({
              showClose: true,
              message: error.data['error'],
              type: "error"
            });
          });
        
        }
      },
      handleClose(done) {
            this.$confirm("确认放弃申请？")
            .then(_ => {
                done();
                console.log(_);
            })
            .catch(_ => {
                console.log(_);
            });
        },

    },

};
</script>

<style lang="scss" scoped>
.info {
  text-align: left;
  font-size: 20px;
}


</style>
