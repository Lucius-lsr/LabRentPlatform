<template>
<<<<<<< HEAD
    <div>
        <el-table
                ref="multipleTable"
                :data="tableData"
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column label="设备编号" width="120">
                <template slot-scope="scope">{{ scope.row.id }}</template>
            </el-table-column>
            <el-table-column prop="name" label="设备名称" width="120"></el-table-column>
            <el-table-column prop="description" label="设备描述" show-overflow-tooltip></el-table-column>
            <el-table-column prop="count" label="设备数量" width="120"></el-table-column>
            <el-table-column prop="provider" label="设备提供者" width="120"></el-table-column>
        </el-table>
=======
  <div>
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column label="设备编号" width="120">
        <template slot-scope="scope">{{ scope.row.id }}</template>
      </el-table-column>
      <el-table-column prop="name" label="设备名称" width="120"></el-table-column>
      <el-table-column prop="description" label="设备描述" show-overflow-tooltip></el-table-column>
      <el-table-column prop="count" label="设备数量" width="120"></el-table-column>
      <el-table-column prop="provider" label="设备提供者" width="120"></el-table-column>
    </el-table>


    <div style="float:left" >
        

    <el-row>

      <el-col :span="3">
        <el-input-number
          style="margin: 30px 5px 0px 20px"
          controls-position="right"
          v-model="applynum"
        
          :min="1"
          :max="10"
          label="数目"
        ></el-input-number>
      </el-col>
      <el-col :span="9">
        <el-input
         style="margin: 30px 0px 0px 150px" v-model="end_time" placeholder="归还日期，例2020-09-07 15:00"></el-input>
      </el-col>
      <el-col :span="9">
        <el-input style="margin: 30px 0px 0px 180px" v-model="reason" placeholder="请输入申请设备的原因"></el-input>
      </el-col>
      <el-col :span="2">
            <el-button style="margin: 30px 5px 0px 200px" type="primary" @click="apply(applynum)">申请</el-button>
        </el-col>
    </el-row>
    <el-row>
        
    </el-row>
    </div>
>>>>>>> a87942dbc942509466c3df6994f8eb8fd91cfc61

        <el-row>

            <el-col :span="8">
                <el-button style="margin: 30px 30px 0px 80px" @click="prePage()">上一页</el-button>
                <el-button @click="nextPage()">下一页</el-button>
            </el-col>
            <el-col :span="4">
                <el-input style="margin: 30px 0px 0px 0px" v-model="inputname"
                          placeholder="请输入需要检索的设备名称"></el-input>
            </el-col>
            <el-col :span="2">
                <el-button style="margin: 30px 5px 0px 0px" type="primary" @click="searchName(inputname)">检索
                </el-button>
            </el-col>
            <el-col :span="1">
                <el-button style="margin: 30px 5px 0px 0px" type="primary" @click="cancleName()">取消
                </el-button>
            </el-col>

        </el-row>

        <div style="float:left; margin-top: 50px">


            <el-row>

                <el-col :span="3">
                    <el-input-number
                            style="margin: 30px 5px 0px 20px"
                            controls-position="right"
                            v-model="applynum"
                            @change="handleChange"
                            :min="1"
                            :max="10"
                            label="数目"
                    ></el-input-number>
                </el-col>
                <el-col :span="9">
                    <div class="block" style="margin: 30px 0px 0px 80px">
                        <el-date-picker
                                v-model="end_time"
                                type="date"
                                placeholder="归还日期">
                        </el-date-picker>
                    </div>
                </el-col>
                <el-col :span="9">
                    <el-input style="margin: 30px 0px 0px 180px" v-model="reason" placeholder="请输入申请设备的原因"></el-input>
                </el-col>
                <el-col :span="2">
                    <el-button style="margin: 30px 5px 0px 200px" type="primary" @click="apply(applynum)">申请</el-button>
                </el-col>
            </el-row>
            <el-row>

            </el-row>
        </div>


    </div>
</template>

<script>
    import api from "../../api";

    export default {
        name: "equipmentlist",
        data() {
            return {
                tableData: [],
                multipleSelection: [],
                inputname: "",
                applynum: 1,
                name: "",
                page: 1,
                total_page: 0,
                end_time: "",
                reason: "",
                pickerOptions: {
                    disabledDate(time) {
                        return time.getTime() > Date.now();
                    },
                    shortcuts: [{
                        text: 'Today',
                        onClick(picker) {
                            picker.$emit('pick', new Date());
                        }
                    }, {
                        text: 'Yesterday',
                        onClick(picker) {
                            const date = new Date();
                            date.setTime(date.getTime() - 3600 * 1000 * 24);
                            picker.$emit('pick', date);
                        }
                    }, {
                        text: 'A week ago',
                        onClick(picker) {
                            const date = new Date();
                            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
                            picker.$emit('pick', date);
                        }
                    }]
                },
            };
        },

        mounted() {
            api.getequipmentlist(1, "").then((res) => {
                //console.log(res)
                this.tableData = res.data.posts;
                this.total_page = res.data.total_page;
                // console.log(this.tableData)
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
            handleChange(value) {
                console.log(value);
            },

            searchName(name) {
                this.name = name;
                api.getequipmentlist(1, name).then((res) => {
                    this.tableData = res.data.posts;
                    this.total_page = res.data.total_page;
                });
            },
            cancleName() {
                this.inputname = "";
                this.name = "";
                api.getequipmentlist(1, "").then((res) => {
                    this.tableData = res.data.posts;
                    this.total_page = res.data.total_page;
                });
            },

            apply(applynum) {
                //   console.log(applynum);
                if (this.$refs.multipleTable.store.states.selection.length < 1) {
                    this.$message("没有勾选要申请的设备！");
                }
                for (
                    var index = 0;
                    index < this.$refs.multipleTable.store.states.selection.length;
                    index++
                ) {
                    var params = {
                        id: this.$refs.multipleTable.store.states.selection[index]["id"],
                        endtime: this.end_time,
                        reason: this.reason,
                        count: applynum,
                    };
                    // console.log(params)
                    api
                        .apply(params)
                        .then((res) => {
                            console.log(res);
                            if (res.status == 200) {
                                this.$message("申请" + params.id + "号设备" + params.count + "台已发送！");
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
                }
            },

            prePage() {
                if (this.page == 1) {
                    alert("当前已是第一页");
                } else {
                    this.page--;
                    api.getequipmentlist(this.page, this.name).then((res) => {
                        this.tableData = res.posts;
                    });
                }
            },
            nextPage() {
                if (this.page == this.total_page) {
                    alert("当前已是最后一页");
                } else {
                    this.page++;
                    api.getequipmentlist(this.page, this.name).then((res) => {
                        this.tableData = res.posts;
                    });
                }
            },
        },
    };
<<<<<<< HEAD
=======
  },

  mounted() {
    api.getequipmentlist(1, "").then((res) => {
      //console.log(res)
      this.tableData = res.data.posts;
      this.total_page = res.data.total_page;
      // console.log(this.tableData)
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
    // handleChange(value) {
    //   console.log(value);
    // },

    searchName(name) {
      this.name = name;
      api.getequipmentlist(1, name).then((res) => {
        this.tableData = res.data.posts;
        this.total_page = res.data.total_page;
      });
    },
    cancleName() {
      this.inputname = "";
      this.name = "";
      api.getequipmentlist(1, "").then((res) => {
        this.tableData = res.data.posts;
        this.total_page = res.data.total_page;
      });
    },

    apply(applynum) {
    //   console.log(applynum);
    if(this.$refs.multipleTable.store.states.selection.length<1)
    {
        this.$message("没有勾选要申请的设备！");
    }
      for (
        var index = 0;
        index < this.$refs.multipleTable.store.states.selection.length;
        index++
      ) {
        var params = {
          id: this.$refs.multipleTable.store.states.selection[index]["id"],
          endtime: this.end_time,
          reason: this.reason,
          count: applynum,
        };
        // console.log(params)
        api
          .apply(params)
          .then((res) => {
            console.log(res);
            if(res.status==200)
            {
                this.$message("申请"+params.id+"号设备"+params.count+"台已发送！");
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
      }
    },

    prePage() {
      if (this.page == 1) {
        alert("当前已是第一页");
      } else {
        this.page--;
        api.getequipmentlist(this.page, this.name).then((res) => {
          this.tableData = res.posts;
        });
      }
    },
    nextPage() {
      if (this.page == this.total_page) {
        alert("当前已是最后一页");
      } else {
        this.page++;
        api.getequipmentlist(this.page, this.name).then((res) => {
          this.tableData = res.posts;
        });
      }
    },
  },
};
>>>>>>> a87942dbc942509466c3df6994f8eb8fd91cfc61
</script>
