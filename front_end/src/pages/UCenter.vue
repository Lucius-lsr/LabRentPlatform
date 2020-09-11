<template>
    <div>
        <div style="margin: 5px">
            <el-card>
                <div slot="header">
          <span v-if="info">
            <span style="float: left;padding: 0px 0px 0px 100px">个人信息</span>
          </span>
                </div>
                <div>你好，用户{{username}}!</div>
                <div v-if="isProvider">
                    <el-row>你拥有设备提供权限</el-row>
                </div>
                <div v-if="!isProvider">
                    <el-row>你没有设备提供权限</el-row>
                </div>
                <br/>
                <br/>
                <br/>

                <el-button style="margin-bottom: 30px" type="danger" @click="logout()">登出</el-button>

                <div>
                    <el-form ref="form" label-width="120px" style="background-color: #eeeeee;padding:20px">
                        <el-form-item label="实验室地址">
                            <el-input v-model="address"></el-input>
                        </el-form-item>
                        <el-form-item label="联系电话">
                            <el-input v-model="phone"></el-input>
                        </el-form-item>
                        <el-form-item label="申请理由">
                            <el-input type="textarea" v-model="textarea"></el-input>
                        </el-form-item>
                        <el-button
                                v-if="!isProvider"
                                type="primary"
                                @click="up_apply()"
                        >申请成为提供者
                        </el-button>
                        <el-button
                                v-else
                                type="primary"
                                @click="up_apply()"
                        >修改并重新申请
                        </el-button>
                    </el-form>

                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
    import api from "../api";

    export default {
        name: "Ucenter",
        data() {
            return {
                info: "",
                address: "",
                phone: "",
                textarea: "",
                username: "",
                isProvider: ""
            };
        },
        mounted() {
            this.username = localStorage.getItem("username");
            this.isProvider = localStorage.getItem("isProvider");
        },
        methods: {
            logout() {
                api
                    .getLogout()
                    .then((res) => {
                        // console.log(res)
                        if (res.status == 200) {
                            this.$message("成功登出");
                            localStorage.setItem("token", "");
                            localStorage.setItem("isProvider", "");
                            this.$router.push("/login");
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
            up_apply() {
                if (!this.textarea || !this.address || !this.phone) {
                    this.$message({
                        showClose: true,
                        message: "申请理由不能为空！",
                        type: "error",
                    });
                    return;
                }

                api
                    .upgrade_apply({
                        lab_info: this.textarea,
                        address: this.address,
                        phone: this.phone,
                    })
                    .then((res) => {
                        if (res.status == 200) {
                            this.$message("您的申请已成功发送！");
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
        },
    };
</script>