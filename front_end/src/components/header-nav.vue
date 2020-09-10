<template>
    <div>
        <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#339999"
            
        >
            <el-menu-item index="5">
                <router-link to="/equipmentlist" tag="li">设备列表</router-link>
            </el-menu-item>
            <!-- <el-menu-item index="1" @click="role()">
            <router-link to="/" tag="li">首页</router-link>
            </el-menu-item> -->
            <el-menu-item index="2">
                <router-link to="/ucenter" tag="li">个人中心</router-link>
            </el-menu-item>
            <!-- <el-menu-item index="3">
                <router-link to="/login" tag="li">登录</router-link>
            </el-menu-item> -->
            <!-- <el-menu-item index="4" v-if="myStore.state.isProvider"> -->
            <el-menu-item index="4" v-if="isProvider">
                <router-link to="/provider" tag="li">设备管理（仅设备提供者可用）</router-link>
            </el-menu-item>
            
            <el-menu-item index="6">
                <router-link to="/applylist" tag="li">申请信息列表</router-link>
            </el-menu-item>
            <el-menu-item index="7">
                <router-link to="/borrowlist" tag="li">租借成功列表</router-link>
            </el-menu-item>
            <el-menu-item index="8">
                <router-link to="/messagelist" tag="li">消息列表</router-link>
            </el-menu-item>
        </el-menu>
    </div>
</template>
<script>

// import store from "../store/index.js"

export default {
    name: "HeaderNav",
    data() {
        return {
            activeIndex: "1",
            isProvider:""
        };
    },
    mounted() {
    this.isProvider = localStorage.getItem("isProvider");
    },
    methods: {
        role(){
            // console.log(this.myStore.state.isProvider)
        }
    }
};
</script>