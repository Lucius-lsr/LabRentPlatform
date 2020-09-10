<template>
    <el-container class="provider">
        <el-aside style="width: 200px; height: 100% "><ProviderNav></ProviderNav></el-aside>
        <el-main><ProviderMain></ProviderMain></el-main>
  </el-container>
</template>

<script>
import ProviderNav from "./ProviderNav"
import ProviderMain from "./ProviderMain"


export default {
  data() {
    return {
    };
  },
  name: "Provider",
  components: {
    ProviderNav,
    ProviderMain
  }
};
</script>

<style lang="scss" scoped>
el-container{
    height: 100%;
}
.el-aside {
  // position: fixed;
  // top: 70px;
  // left: 0;
  background-color: #fff;
  width: 200px;
  color: #333;
  text-align: center;
  line-height: 200px;
  height: 90vh;
  border-width: 1px;
  border-left-width: 0px;
  border-style: solid;
  border-color: rgb(177, 177, 177);
}
</style>
