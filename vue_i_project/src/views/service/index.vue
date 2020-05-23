<template>
    <div class="service-main">
        <el-button @click="openAddModal">创建服务</el-button>
        <el-table
                :data="serviceList.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
                style="width: 100%">
            <el-table-column
                    label="名称"
                    prop="name">
                <template slot-scope="scope">
                    <a href="javascript:void(0)" style='text-decoration:none;' @click="goToInterface(scope.row.id)">{{scope.row.name}}</a>
                </template>
            </el-table-column>
            <el-table-column
                    label="描述"
                    prop="description">
            </el-table-column>
            <el-table-column
                    align="right">
                <template slot="header" slot-scope="scope">
                    {{scope.row}}
                    <el-input
                            v-model="search"
                            size="mini"
                            placeholder="输入关键字搜索"/>
                </template>
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="openEditModal(scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="deleteServiceFun(scope.row.id)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
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
    import {addService, deleteService, getAllService, updateService} from "../../request/service";

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
                search: '',
                total: 0,
                pagesize: 10,
                currentPage: 1,
            }
        },
        methods: {
            handleSizeChange: function (pagesize) {
                this.pagesize = pagesize;
                this.getAllServiceFun(this.currentPage, this.pagesize)
                console.log(this.pagesize)  //每页下拉显示数据
            },
            handleCurrentChange: function (currentPage) {
                this.currentPage = currentPage;
                this.getAllServiceFun(currentPage, this.pagesize)
                console.log(this.currentPage)  //点击第几页
            },
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
                                this.getAllServiceFun(this.currentPage, this.pagesize)
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
            editServiceFun() { //这是请求编辑服务
                this.$refs.editFormRef.validate((valid) => {
                    if (valid) {
                        updateService(this.editForm.id, this.editForm).then(data => {
                            let success = data.data.success
                            if (success) {
                                this.dialogEditVisible = false;
                                this.getAllServiceFun(this.currentPage, this.pagesize)
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
            // 获取所有服务
            getAllServiceFun(page, pageSize) {
                getAllService(page, pageSize).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.serviceList = data.data.data;
                        this.total = data.data.count;
                        console.log(this.total)
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
            },
            // 删除服务提示
            deleteServiceFun(serviceId) {
                this.$confirm('此操作将永久删除该服务, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    //确定删除
                    deleteService(serviceId).then(data => {
                        let success = data.data.success
                        if (success) {
                            this.getAllServiceFun(this.currentPage, this.pagesize)
                            this.$message({
                                message: '删除成功',
                                type: 'success'
                            });
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

            goToInterface(serviceId) {
                this.$router.push(`/interface/?serviceId=${serviceId}`)
            },
        }
        ,


        created() {
            this.getAllServiceFun(1, 10);
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

    .pagestyle {
        /*margin-top: 50px;*/
        /*margin-right: -50px;*/
        padding: 100px 10px 10px 900px;
    }
</style>