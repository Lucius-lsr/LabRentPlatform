
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
        <template slot-scope="scope">{{ scope.row.end_time }}</template>
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
    };
  },

  mounted() {
    api
      .getborrowlist()
      .then((res) => {
        this.tableData = res.posts;
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
  },
};
</script>
