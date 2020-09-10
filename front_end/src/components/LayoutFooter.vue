<template>
  <div class="footer">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-size="10"
      layout="total, prev, pager, next, jumper"
      :total="totalPost"
      background
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
      this.$emit("changePage", val);
    }
  },
  data() {
    return {
      currentPage: 1
    };
  },
  name: "layoutFooter",
  props: ["totalPost"]
};
</script>
<style lang="scss" scoped>
.footer {
  margin-top: 20px;
}
</style>
