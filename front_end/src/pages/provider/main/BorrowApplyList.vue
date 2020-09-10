<template>
  <div class="borrowapplylist">
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="申请ID" width="150"></el-table-column>
      <el-table-column prop="target_equipment.name" label="设备名称"></el-table-column>
      <el-table-column prop="count" label="设备数目" width="150"></el-table-column>
      <el-table-column prop="endtime" label="归还时间" width="200"></el-table-column>
      <el-table-column prop="borrower" label="申请人" width="150"></el-table-column>
      <el-table-column prop="state" label="状态" width="150">
        <template slot-scope="scope">
          <div v-if="scope.row.state === 0" style="color=rgb(245, 245, 245)">等待确认</div>
          <div v-if="scope.row.state === 1" style="color=green">已租借</div>
          <div v-if="scope.row.state === 2" style="color=red">已拒绝</div>
          <div v-if="scope.row.state === 3" style="color=rgb(132, 43, 226)">已归还</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template slot-scope="scope">
          <el-button type="primary" @click="handleDetails(scope.$index)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="tableData[0]">
      <el-dialog title="租借申请" :visible.sync="dialogVisible" style="font-size: 30px;">
        <el-row class="info">申请ID: {{ tableData[currentIndex].id }}</el-row>
        <el-row class="info">设备:</el-row>
        <el-row class="info">
          <el-col :offset="2">ID: {{ tableData[currentIndex].target_equipment.id }}</el-col>
        </el-row>
        <el-row class="info">
          <el-col :offset="2">名称: {{ tableData[currentIndex].target_equipment.name }}</el-col>
        </el-row>
        <el-row class="info">
          <el-col :offset="2">总数: {{ tableData[currentIndex].target_equipment.count }}</el-col>
        </el-row>
        <el-row class="info">
          <el-col :offset="2">描述: {{ tableData[currentIndex].target_equipment.description }}</el-col>
        </el-row>
        <el-row class="info">申请租借数目: {{ tableData[currentIndex].count }}</el-row>
        <el-row class="info">归还时间: {{ tableData[currentIndex].endtime }}</el-row>
        <el-row class="info">申请人: {{ tableData[currentIndex].borrower }}</el-row>
        <el-row class="info">
          申请状态：
          <el-col
            :offset="2"
            v-if="tableData[currentIndex].state=== 0"
            style="color=rgb(245, 245, 245)"
          >等待确认</el-col>
          <el-col :offset="2" v-if="tableData[currentIndex].state=== 1" style="color=green">已租借</el-col>
          <el-col :offset="2" v-if="tableData[currentIndex].state=== 2" style="color=red">已拒绝</el-col>
          <el-col
            :offset="2"
            v-if="tableData[currentIndex].state=== 3"
            style="color=rgb(132, 43, 226)"
          >已归还</el-col>
        </el-row>
        <el-row class="info">申请原因：</el-row>
        <el-row class="info">
          <el-col :offset="2">{{tableData[currentIndex].reason}}</el-col>
        </el-row>
        <el-row :gutter="10" class="info">
          <el-col>是否同意租借？</el-col>
          <el-col :span="3" :offset="2">
            <el-button type="success" @click="whetherAgree(1,tableData[currentIndex].id)">同意</el-button>
          </el-col>
          <el-col :span="3">
            <el-button type="danger" @click="whetherAgree(2,tableData[currentIndex].id)">拒绝</el-button>
          </el-col>
        </el-row>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">确定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import api from "../../../api/index";

export default {
  name: "BorrowApplyList",
  components: {
    // layoutFooter
  },
  data() {
    return {
      tableData: [],
      //   totalPost: 0,
      //   page: 1,
      dialogVisible: false,
      currentIndex: 0,
    };
  },
  mounted() {
    this.getList();
  },
  methods: {
    getList() {
      api
        .getBorrowApplyList()
        .then((res) => {
          //   this.page = res.data.page;
          //   this.totalPost = res.data.total_page;
          this.tableData = res.data.borrow_apply_list;
        })
        .catch((error) => {
          if (error.response) {
            //返回错误code
            this.$message({
              showClose: true,
              message: error.response.data.message,
              type: "error",
            });
          } else {
            this.$message({
              showClose: true,
              message: error.data["error"],
              type: "error",
            });
          }
        });
    },
    //   changePage(page) {
    //     this.page = page;
    //     this.getList();
    //   },
    handleDetails(index) {
      // console.log(index, row);
      this.currentIndex = index;
      this.dialogVisible = true;
    },
    whetherAgree(tag, id) {
      let that = this;
      if (tag === 1) {
        that
          .$confirm("确认同意？", "确认信息", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          })
          .then(() => {
            let params = {
              id: id,
              flag: tag,
            };
            api
              .agreeBorrowApply(params)
              .then((res) => {
                that.$message({
                  type: "success",
                  message: res.data["message"] + "已同意申请!",
                });
                that.getList();
                that.dialogVisible = false;
              })
              .catch((error) => {
                that.$message({
                  showClose: true,
                  message: error.data["error"],
                  type: "error",
                });
              });
          })
          .catch(() => {
            that.$message({
              type: "info",
              message: "已取消",
            });
          });
      } else {
        that
          .$confirm("确认拒绝？", "确认信息", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          })
          .then(() => {
            let params = {
              id: id,
              flag: tag,
            };
            api
              .agreeBorrowApply(params)
              .then((res) => {
                if (res.status == 200) {
                  // console.log(res)
                  that.$message({
                    type: "error",
                    message: "已拒绝申请!",
                  });
                  that.getList();
                  that.dialogVisible = false;
                }
              })
              .catch((error) => {
                that.$message({
                  showClose: true,
                  message: error.data["error"],
                  type: "error",
                });
              });
          })
          .catch(() => {
            that.$message({
              type: "info",
              message: "已取消",
            });
          });
      }
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
