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
            <el-menu-item index="1">
                <router-link to="/equipmentlist" tag="li">设备列表</router-link>
            </el-menu-item>


            <el-menu-item index="3" >
                <router-link to="/applylist" tag="li">申请列表</router-link>
            </el-menu-item>

            <el-menu-item index="4">
                <router-link to="/borrowlist" tag="li">租借列表</router-link>
            </el-menu-item>

            <el-menu-item index="5">
                <router-link to="/messagelist" tag="li">消息列表</router-link>
            </el-menu-item>

            <el-menu-item index="6" v-if="isProvider" style="float:right">
                <router-link to="/provider" tag="li">我的设备管理</router-link>
            </el-menu-item>

            <el-menu-item index="7" style="float:right">
                <router-link to="/ucenter" tag="li">个人中心</router-link>
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
                isProvider: ""
            };
        },
        mounted() {
            this.isProvider = localStorage.getItem("isProvider");
        },
        methods: {
            role() {
                // console.log(this.myStore.state.isProvider)
            }
        }
    };
</script>