<template>
    <div class="service-main">
        <el-button @click="openAddModal">创建服务</el-button>
        <div class="service-list">
            <el-card class="service-card" v-for="item in serviceList" :key="item.id">
                <div slot="header" class="service-card-header">
                    <div>{{item.name}}</div>
                    <el-button style="padding: 3px 0;" type="text" @click="openEditModal(item)">编辑
                    </el-button>
                    <el-button style=" padding: 3px 0;margin-left: 5px;
                    " type="text">删除
                    </el-button>
                </div>
                <div>
                    {{item.description}}
                </div>
            </el-card>
        </div>

        <el-dialog title="创建服务" :visible.sync="dialogAddVisible">
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
                <el-button type="primary" @click="addServiceFun">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog title="编辑服务" :visible.sync="dialogEditVisible">
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
                <el-button type="primary" @click="editServiceFun">确 定</el-button>
            </div>
        </el-dialog>


    </div>
</template>

<script>
    import {addService, getAllService, updateService} from "../../request/service";

    export default {
        name: "service",
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
                        {required: true, message: '请输入服务名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请填写服务描述', trigger: 'blur'}
                    ]
                },
                editForm: {
                    id: 0,
                    name: "",
                    description: "",
                },
                editRules: {
                    name: [
                        {required: true, message: '请输入服务名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请填写服务描述', trigger: 'blur'}
                    ]
                },
                serviceList: [],
            }
        },
        methods: {
            openAddModal() { //这是打开创建服务窗口
                this.dialogAddVisible = true
            },
            openEditModal(data) { //这是打开编辑服务窗口
                this.dialogEditVisible = true
                // 此处是编辑时回显到输入框
                this.editForm.id = data.id
                this.editForm.name = data.name
                this.editForm.description = data.description
            },
            addServiceFun() { //这是请求创建服务
                // 代表addFormRef表单的控件属性
                this.$refs.addFormRef.validate((valid) => {
                    if (valid) {
                        addService(this.addForm).then(data => {
                            let success = data.data.success
                            if (success) {
                                this.dialogAddVisible = false;
                                this.getAllServiceFun()
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
            editServiceFun() { //这是请求编辑服务
                this.$refs.editFormRef.validate((valid) => {
                    if (valid) {
                        updateService(this.editForm.id, this.editForm).then(data => {
                            let success = data.data.success
                            if (success) {
                                this.dialogEditVisible = false;
                                this.getAllServiceFun()

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
            // 获取所有服务
            getAllServiceFun() {
                getAllService().then(data => {
                    let success = data.data.success
                    if (success) {
                        this.serviceList = data.data.data;
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
            }
        },

        created() {
            this.getAllServiceFun();
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
    .service-main {
        text-align: left;
        padding: 5px 5px;
    }

    .service-card {
        width: 250px;
        margin-top: 5px;
        margin-right: 10px;
    }

    .service-list {
        display: flex;
        flex-wrap: wrap;
    }

    .service-card-header {
        display: flex;
        justify-content: space-between;
    }
</style>