<template>
    <div class="lendlist">
        <el-table
                :data="tableData"
                border
                style="width: 100%"
        >
            <el-table-column prop="id" label="申请ID" width="150"></el-table-column>
            <el-table-column prop="target_equipment.name" label="设备名称"></el-table-column>
            <el-table-column prop="count" label="设备数目" width="150"></el-table-column>
            <el-table-column prop="endtime" label="归还时间" width="200"></el-table-column>
            <el-table-column prop="borrower" label="申请人" width="150"></el-table-column>
            <el-table-column prop="state" label="状态" width="150">
                <template slot-scope="scope">
                    <div v-if="scope.row.state === 1" style="color:green">已租借</div>
                    <div v-if="scope.row.state === 3" style="color:rgb(132, 43, 226)">已归还</div>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
                <template slot-scope="scope">
                    <el-button
                            type="primary"
                            @click="handleDetails(scope.$index)">详情
                    </el-button>
                    <el-button
                            type="success"
                            v-if="scope.row.state === 1"
                            @click="handleReturn(scope.row)">确认归还
                    </el-button>
                </template>
            </el-table-column>

        </el-table>


        <div v-if="tableData[0]">
            <el-dialog
                    title="租借申请"
                    :visible.sync="dialogVisible"
                    style="font-size: 30px;"
            >

                <table style="font-size: 20px">
                    <tr>
                        <th>申请ID：</th>
                        <td>{{ tableData[currentIndex].id }}</td>
                    </tr>
                    <tr>
                        <th>设备ID：</th>
                        <td>{{ tableData[currentIndex].target_equipment.id }}</td>
                    </tr>
                    <tr>
                        <th>设备名称：</th>
                        <td>{{ tableData[currentIndex].target_equipment.name }}</td>
                    </tr>
                    <tr>
                        <th>设备剩余：</th>
                        <td>{{ tableData[currentIndex].target_equipment.count }}</td>
                    </tr>
                    <tr>
                        <th>设备描述：</th>
                        <td>{{ tableData[currentIndex].target_equipment.description }}</td>
                    </tr>
                    <tr>
                        <th>申请租借数目：</th>
                        <td>{{ tableData[currentIndex].count }}</td>
                    </tr>
                    <tr>
                        <th>归还时间：</th>
                        <td>{{ tableData[currentIndex].endtime }}</td>
                    </tr>
                    <tr>
                        <th>申请人：</th>
                        <td>{{ tableData[currentIndex].borrower }}</td>
                    </tr>
                    <tr>
                        <th>申请状态：</th>
                        <td v-if="tableData[currentIndex].state=== 1" style="color:green">已租借</td>
                        <td v-if="tableData[currentIndex].state=== 3" style="color:rgb(132, 43, 226)">已归还</td>
                    </tr>
                    <tr>
                        <th>申请原因：</th>
                        <td>{{tableData[currentIndex].reason}}</td>
                    </tr>
                </table>

                <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确定</el-button>
      </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>

    import api from "../../../api/index"

    export default {
        name: "LendList",
        data() {
            return {
                tableData: [],
                dialogVisible: false,
                currentIndex: 0
            }
        },
        mounted() {
            this.getList();
        },
        methods: {
            getList() {
                api.getLendList()
                    .then(res => {
                        this.tableData = res.data.posts;
                    })
                    .catch(error => {
                        this.$message({
                            showClose: true,
                            message: error.data['error'],
                            type: "error"
                        });
                    })
            },
            handleDetails(index) {
                this.currentIndex = index;
                this.dialogVisible = true;
            },
            handleReturn(row) {
                let pramas = {
                    id: row.id
                }
                api.confirmReturn(pramas)
                    .then(res => {
                        this.$message({
                            showClose: true,
                            message: res.data.message + "已确认",
                            type: "success"
                        });
                        this.getList();
                    })
                    .catch(error => {
                        this.$message({
                            showClose: true,
                            message: error.data['error'],
                            type: "error"
                        });
                    })
            }

        },
    };
</script>

<style lang="scss" scoped>
    .info {
        text-align: left;
        font-size: 20px;
        margin-top: 10px;
    }

    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }
</style>
