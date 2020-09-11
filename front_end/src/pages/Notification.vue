<template>
    <div>
        <div v-if="!messages.length">
            当前无通知
        </div>
        <div v-if="messages.length">
            <div v-for="index in (0,messages.length)" :key="index">
                <div style="margin: 5px" v-if="messages[index-1]">
                    <el-card class="box-card" :id="color(messages[index-1].state)">
                        <div slot="header">
                <span
                        width="30%"
                        style="float: left"
                >类型:  {{change(messages[index-1].type)}}</span>

                            <span>
                  结果:{{state(messages[index-1].state)}}
              </span>
                        </div>
                        <div class="text item" v-if="messages[index-1].apply">
                            {{ equipment_details(messages[index-1].apply.target_equipment)}}
                        </div>
                        <br/>
                        <div v-if="messages[index-1].apply">
                            <div class="text item" v-if="messages[index-1].apply.remarks">
                                申请理由：{{messages[index-1].apply.remarks}}
                            </div>
                            <div class="text item" v-if="messages[index-1].apply.reason">
                                申请理由：{{messages[index-1].apply.reason}}
                            </div>
                        </div>
                    </el-card>
                </div>
            </div>
        </div>


    </div>
</template>

<script>
    import api from "../api";

    export default {
        name: "Notification",
        data() {
            return {
                messages: []
            }
        },
        mounted() {
            api.notice().then((res) => {
                this.messages = res.data.notification;
            })
        },
        methods: {
            state(state) {
                if (state == 1) return '成功'
                if (state == 2) return '拒绝'
            },
            change(state) {
                state = String(state)

                if (state == "borrow apply") return '租借申请'
                if (state == "onshelf apply") return '上架申请'
                if (state == "upgrade apply") return '升级申请'
            },
            color(state) {
                state = String(state)
                if (state == 2) return "redtype"
                if (state == 1) return "greentype"
            },
            equipment_details(e) {
                return `id: ${e['id']} 名称：${e['name']} 简介：${e['description']} 数量：${e['count']} 提供者：${e['provider']} `
            }
        },
    };
</script>
<style>
    .bank {
        padding-left: 1.8em;
    }

    .text {
        font-size: 14px;
    }

    .item {
        font-size: 13px;
        float: left;
    }

    .box-card {
        width: 100%;
    }

    #redtype {
        background-color: salmon;

    }

    #greentype {
        background-color: springgreen;
    }
</style>