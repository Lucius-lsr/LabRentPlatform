<template>
    <div>
        <div class="important">设备租赁智能管理平台</div>
        <HeaderNav></HeaderNav>
        <router-view></router-view>
    </div>
</template>
<script>
import HeaderNav from "../components/header-nav"

export default {
  name: 'Layout',
  components: {
    HeaderNav
  }
}
</script>

<style>
    .important
    {
        font-size: 36px;
        
        margin:0px 0px 30px 0px;
    }
</style>