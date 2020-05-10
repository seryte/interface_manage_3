<template>
    <div class="task-main">
        <el-button @click="openAddModal">创建任务</el-button>
        <div class="task-list">
            <el-card class="task-card" v-for="item in taskList" :key="item.id">
                <div slot="header" class="task-card-header">
                    <div>{{item.name}}</div>
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
                </div>
            </el-card>
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


    </div>
</template>

<script>
    import {addTask, deleteTask, getAllTask, updateTask} from "../../request/task";

    export default {
        name: "task",
        data() {
            return {
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
            }
        },
        methods: {
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
                                this.getAllTaskFun()
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
                                this.getAllTaskFun()

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
            getAllTaskFun() {
                getAllTask().then(data => {
                    let success = data.data.success
                    if (success) {
                        this.taskList = data.data.data;
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
                            this.getAllTaskFun()
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
        },


        created() {
            this.getAllTaskFun();
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
</style>