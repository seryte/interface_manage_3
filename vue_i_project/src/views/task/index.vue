<template>
    <div class="task-main">
        <el-button @click="openAddModal">创建任务</el-button>
        <div class="task-list">
            <el-card class="task-card" v-for="item in taskList" :key="item.id">
                <div slot="header" class="task-card-header">
                    <div>
                        <a href="javascript:void(0)" @click="showDrawer(item.id)" style='text-decoration:none;'>{{item.name}}</a>
                    </div>
                    <div>
                        <el-button style="padding: 3px 0;" type="text" @click="openEditModal(item)">编辑
                        </el-button>
                        <el-button style=" padding: 3px 0;margin-left: 5px;
                    " type="text" @click="deleteTaskFun(item.id)">删除
                        </el-button>
                    </div>
                </div>
                <div>
                    {{item.description}}
                    <div>
                        <a href="javascript:void(0)" @click="showReport(item.id)"
                           style='text-decoration:none;'>查看报告</a>
                    </div>
                </div>

            </el-card>
        </div>
        <div class="pagestyle">
            <el-pagination
                    background
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[5, 10, 50, 100]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>
        </div>

        <el-dialog title="创建任务" :visible.sync="dialogAddVisible">
            <el-form :model="addForm" :rules="addRules" ref="addFormRef" label-width="50px" class="demo-addForm">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>

                <el-form-item label="描述" prop="description">
                    <el-input v-model="addForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogAddVisible = false">取 消</el-button>
                <el-button type="primary" @click="addTaskFun">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog title="编辑任务" :visible.sync="dialogEditVisible">
            <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="50px" class="demo-editForm">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>

                <el-form-item label="描述" prop="description">
                    <el-input v-model="editForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogEditVisible = false">取 消</el-button>
                <el-button type="primary" @click="editTaskFun">确 定</el-button>
            </div>
        </el-dialog>
        <!--这里是关联任务的抽屉-->
        <el-drawer
                :visible.sync="drawerShowFlag"
                direction="rtl"
                size="40%">
            <!--            slot是插槽，占位符的感觉，这里等于重写了title-->
            <div slot="title">
                <el-button type="primary" @click="showAddInterface=true">关联接口</el-button>
            </div>
            <el-table
                    :data="interfaces"
                    stripe
                    style="width: 100%">
                <el-table-column
                        prop="name"
                        label="名称"
                        min-width="40%">
                </el-table-column>

                <el-table-column
                        label="URL"
                        min-width="45%">
                    <template slot-scope="scope">
                        {{scope.row.context.url}}
                    </template>
                </el-table-column>

                <el-table-column label="操作" min-width="15%">
                    <template slot-scope="scope">
                        <el-button
                                @click="deleteTaskInterfaceFun(scope.row)"
                                size="mini"
                                type="danger">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

        </el-drawer>

        <!--        这里是查看报告的抽屉-->
        <el-drawer
                :visible.sync="reportShowFlag"
                direction="rtl"
                size="40%">
            <!--            slot是插槽，占位符的感觉，这里等于重写了title-->
            <div slot="title">
                <el-button type="primary" @click="runTaskFun()" v-loading.fullscreen.lock="fullscreenLoading" plain>执行任务</el-button>
            </div>
            <el-table
                    :data="reports"
                    stripe
                    style="width: 100%">
                <el-table-column
                        prop="name"
                        label="名称"
                        min-width="40%">
                    <template slot-scope="scope">
                        <!--后端写死的需要优化-->
                        <a :href="'http://localhost:8000/api/task/'+currentTaskId+'/report/'+scope.row+'/'"
                           target="_blank">{{scope.row}}</a>
                    </template>
                </el-table-column>
            </el-table>

        </el-drawer>

        <el-dialog
                title="关联接口"
                :visible.sync="showAddInterface"
                width="40%">
            <selectInterface ref="selectInterface"></selectInterface>
            <span slot="footer" class="dialog-footer">
                <el-button @click="showAddInterface = false">取 消</el-button>
                <el-button type="primary" @click="addTaskInterfacesFun">确 定</el-button>
              </span>
        </el-dialog>
    </div>
</template>

<script>
    import {addTask, deleteTask, getAllTask, updateTask} from "../../request/task";
    import {
        addTaskInterface,
        deleteTaskInterface,
        getTaskInterface,
        getTaskReports,
        runTask
    } from "../../request/taskInterface";
    import selectInterface from "./selectInterface"

    export default {
        name: "task",
        components: {
            selectInterface
        },
        data() {
            return {
                table: false,
                dialogAddVisible: false,
                dialogEditVisible: false,
                addForm: {
                    name: "",
                    description: "",
                },
                addRules: {
                    name: [
                        {required: true, message: '请输入任务名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请填写任务描述', trigger: 'blur'}
                    ]
                },
                editForm: {
                    id: 0,
                    name: "",
                    description: "",
                },
                editRules: {
                    name: [
                        {required: true, message: '请输入任务名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请填写任务描述', trigger: 'blur'}
                    ]
                },
                taskList: [],
                interfaces: [],
                drawerShowFlag: false,
                reportShowFlag: false,
                reports: [],
                showAddInterface: false,
                currentTaskId: 0,
                total: 0,
                pagesize: 10,
                currentPage: 1,
                fullscreenLoading: false,
            }
        },
        methods: {
            handleSizeChange: function (pagesize) {
                this.pagesize = pagesize;
                this.getAllTaskFun(this.currentPage, this.pagesize)
                console.log("显示 " + this.pagesize + "条")  //每页下拉显示数据
            },
            handleCurrentChange: function (currentPage) {
                this.currentPage = currentPage;
                this.getAllTaskFun(this.currentPage, this.pagesize)
                console.log(this.currentPage)  //点击第几页
            },
            addTaskInterfacesFun() {
                let multipleSelection = this.$refs.selectInterface.multipleSelection
                let req = []
                for (let i = 0; i < multipleSelection.length; i++) {
                    req.push({task_id: this.currentTaskId, interface_id: multipleSelection[i].id})
                }
                if (req.length === 0) {
                    return
                }
                addTaskInterface(req).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.showAddInterface = false
                        this.showDrawer(this.currentTaskId)
                        this.$message({
                            message: '创建成功',
                            type: 'success'
                        });
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
            },
            showDrawer(taskId) {
                this.currentTaskId = taskId,
                    getTaskInterface(taskId).then(data => {
                        let success = data.data.success
                        if (success) {
                            this.interfaces = data.data.data;
                        } else {
                            this.$notify.error({
                                title: "错误",
                                message: data.data.error.message
                            })
                        }
                    })
                this.drawerShowFlag = true;

            },
            deleteTaskInterfaceFun(taskInterface) {
                this.$confirm('此操作将永久删除该接口, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    //确定删除
                    deleteTaskInterface(taskInterface.task_interface_id).then(data => {
                        let success = data.data.success
                        if (success) {

                            this.$message({
                                message: '删除成功',
                                type: 'success'
                            });
                            this.showDrawer(taskInterface.task_id)
                        } else {
                            this.$notify.error({
                                title: "错误",
                                message: data.data.error.message
                            })
                        }
                    })
                }).catch(() => {
                    //取消删除
                });
            },
            openAddModal() { //这是打开创建任务窗口
                this.dialogAddVisible = true
            },
            openEditModal(data) { //这是打开编辑任务窗口
                this.dialogEditVisible = true
                // 此处是编辑时回显到输入框
                this.editForm.id = data.id
                this.editForm.name = data.name
                this.editForm.description = data.description
            },
            addTaskFun() { //这是请求创建任务
                // 代表addFormRef表单的控件属性
                this.$refs.addFormRef.validate((valid) => {
                    if (valid) {
                        addTask(this.addForm).then(data => {
                            let success = data.data.success
                            if (success) {
                                this.dialogAddVisible = false;
                                this.getAllTaskFun(this.currentPage, this.pagesize)
                                this.$message({
                                    message: '创建成功',
                                    type: 'success'
                                });
                            } else {
                                this.$notify.error({
                                    title: "错误",
                                    message: data.data.error.message
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });

            },
            editTaskFun() { //这是请求编辑任务
                this.$refs.editFormRef.validate((valid) => {
                    if (valid) {
                        updateTask(this.editForm.id, this.editForm).then(data => {
                            let success = data.data.success
                            if (success) {
                                this.dialogEditVisible = false;
                                this.getAllTaskFun(this.currentPage, this.pagesize)
                                this.$message({
                                    message: '修改成功',
                                    type: 'success'
                                });

                            } else {
                                this.$notify.error({
                                    title: "错误",
                                    message: data.data.error.message
                                })
                            }
                        })
                    } else {
                        return false;
                    }
                });
            },
            // 获取所有任务
            getAllTaskFun(size, pageSize) {
                getAllTask(size, pageSize).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.taskList = data.data.data;
                        this.total = data.data.count;
                        this.useTotal = this.total;
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
            },
            // 删除任务提示
            deleteTaskFun(taskId) {
                this.$confirm('此操作将永久删除该任务, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    //确定删除
                    deleteTask(taskId).then(data => {
                        let success = data.data.success
                        if (success) {
                            this.$message({
                                message: '删除成功',
                                type: 'success'
                            });
                            this.getAllTaskFun(this.currentPage, this.pagesize)
                        } else {
                            this.$notify.error({
                                title: "错误",
                                message: data.data.error.message
                            })
                        }
                    })
                }).catch(() => {
                    //取消删除
                });
            },

            showReport(taskId) {
                this.currentTaskId = taskId;
                getTaskReports(taskId).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.reports = data.data.data
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
                this.reportShowFlag = true;
            },
            runTaskFun() {
                this.fullscreenLoading = true
                runTask(this.currentTaskId).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.showReport(this.currentTaskId)
                        this.$message({
                            message: '执行成功',
                            type: 'success'
                        });
                        this.getAllTaskFun(this.currentPage, this.pagesize)
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                    this.fullscreenLoading = false
                })

            },
        },


        created() {
            this.getAllTaskFun(1, 10);
        }
    }
</script>
<style>
    .el-card__header {
        padding: 10px 20px;
        border-bottom: 1px solid #EBEEF5;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
    }
</style>
<style scoped>
    .task-main {
        text-align: left;
        padding: 5px 5px;
    }

    .task-card {
        width: 250px;
        margin-top: 5px;
        margin-right: 10px;
    }

    .task-list {
        display: flex;
        flex-wrap: wrap;
    }

    .task-card-header {
        display: flex;
        justify-content: space-between;
    }

    .pagestyle {
        /*margin-top: 50px;*/
        /*margin-right: -50px;*/
        padding: 100px 10px 10px 900px;
    }
</style>