
<template>
  <div>
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="申请数量" width="60">
        <template slot-scope="scope">{{ scope.row.count }}</template>
      </el-table-column>
      <el-table-column label="设备编号" width="60">
        <template slot-scope="scope">{{ scope.row.target_equipment.id }}</template>
      </el-table-column>
      <el-table-column label="设备名称" width="120">
        <template slot-scope="scope">{{ scope.row.target_equipment.name }}</template>
      </el-table-column>
      <el-table-column label="设备描述" width="120">
        <template slot-scope="scope">{{ scope.row.target_equipment.description }}</template>
      </el-table-column>
      <el-table-column label="设备数量" width="60">
        <template slot-scope="scope">{{ scope.row.target_equipment.count }}</template>
      </el-table-column>
      <el-table-column label="设备提供者" width="120">
        <template slot-scope="scope">{{ scope.row.target_equipment.provider }}</template>
      </el-table-column>
      <el-table-column label="归还时间" width="120">
        <template slot-scope="scope">{{ scope.row.endtime }}</template>
      </el-table-column>
      <el-table-column label="是否即将到期" width="120">
        <template slot-scope="scope">{{ scope.row.state }}</template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 20px">
      <el-button @click="toggleSelection()">取消勾选</el-button>
    </div>
  </div>
</template>

<script>
import api from "../../api";

export default {
  name: "borrowlist",
  data() {
    return {
      tableData: [],
      multipleSelection: [],
      //   hurry: [],
    };
  },

  mounted() {
    api
      .getborrowlist()
      .then((res) => {
        if (res.status == 200) {
          this.tableData = res.data.posts;
          console.log(this.tableData);
          var d = new Date();
          var nowyear = d.getFullYear();
          var nowmonth = d.getMonth() + 1;
          var nowday = d.getDate();
          for (var index = 0; index < this.tableData.length; index++) {
            if (
              this.ifhurry(
                nowyear,
                nowmonth,
                nowday,
                this.tableData[index].endtime
              )
            ) {
              this.tableData[index].state = "是";
            }
            // console.log(this.hurry[index]);
            else {
              this.tableData[index].state = "否";
            }
          }
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

  methods: {
    toggleSelection(rows) {
      if (rows) {
        rows.forEach((row) => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    ifhurry(year, month, day, endtime) {
      var timestr = String(endtime);
      var year2 = Number(timestr.substring(0, 4));
      var month2 = Number(timestr.substring(5, 7));
      var day2 = Number(timestr.substring(8, 10));
      // console.log(year2)
      // console.log(month2)
      // console.log(day2)
      var isbig = 0;
      if (year < year2) isbig = 1;
      else if (year > year2) isbig = 0;

      if (year == year2) {
        if (month < month2) isbig = 1;
        else if (month > month2) isbig = 0;
        else {
          if (day < day2) isbig = 1;
        }
      }
      if (isbig) {
        var remains = (year2 - year) * 365 + (month2 - month) * 30 + day2 - day;
        // console.log(remains)
        if (remains >= 0 && remains < 8) return true;
      }
      return false;
    },
  },
};
</script>
