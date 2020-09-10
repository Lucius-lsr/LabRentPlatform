<template>
  <div class="equipmentlist">
        <div style="margin: 10px"></div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
    >
      <el-table-column prop="id" label="设备id" width="150"> </el-table-column>
      <el-table-column prop="name" label="设备名称" ></el-table-column>
      <el-table-column prop="count" label="设备数目" width="150"></el-table-column>
      <!-- <el-table-column prop="provider" label="设备提供者" width="200"></el-table-column> -->
      <el-table-column label="操作" width="150"><template slot-scope="scope">
        <el-button
          type="primary"
          @click="handleEdit(scope.$index, scope.row)">查看详情</el-button>
      </template></el-table-column>
      
    </el-table>
    
    <el-footer
      ><layoutFooter
        :totalPost="totalPost"
        @changePage="changePage"
      ></layoutFooter
    ></el-footer>
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
      totalPost: 0,
      page: 1,
      searchName: ""
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
          this.totalPost = res.data.total_page;
          this.tableData = res.data.posts;
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
      search(){
        let params = {
          page: this.page,
          name: this.searchName
        };
        this.loadList(params); 
      }
    },

};
</script>

<style lang="scss" scoped></style>
