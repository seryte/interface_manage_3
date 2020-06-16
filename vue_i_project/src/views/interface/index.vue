<template>
    <div class="interface_main">
        <el-button @click="openAddModal">创建接口</el-button>
        <el-table
                :data="interfaces"
                style="width: 100%">
            <el-table-column
                    prop="name"
                    label="名称"
                    width="180">
            </el-table-column>
            <el-table-column
                    prop="description"
                    label="描述">
            </el-table-column>

            <el-table-column
                    label="URL">
                <template slot-scope="scope">
                    <a :href="scope.row.context.url" target="_blank">{{scope.row.context.url}}</a>
                </template>
            </el-table-column>

            <el-table-column
                    label="所属服务">
                <template slot-scope="scope">
                    {{scope.row.service_name}}
                </template>
            </el-table-column>

            <el-table-column label="操作" width="200">
                <template slot-scope="scope">
                    <el-button
                            @click="openEditDialog(scope.row)"
                            size="mini">编辑
                    </el-button>
                    <el-button
                            @click="deleteInterfaceFun(scope.row.id)"
                            size="mini"
                            type="danger">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog
                title="新建接口"
                :visible.sync="addDialogVisible"
                width="40%">
            <el-form :model="addForm" :rules="rules" ref="addRuleForm" label-width="100px">
                <el-form-item label="接口名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>

                <el-form-item label="接口描述" prop="description">
                    <el-input v-model="addForm.description"></el-input>
                </el-form-item>

                <el-form-item label="接口详情" prop="context">
                    <editor v-model="addForm.context" @init="editorInit" lang="json" theme="chrome" width="450"
                            height="200"></editor>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAddInterface">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog
                title="编辑接口"
                :visible.sync="editDialogVisible"
                width="40%">
            <el-form :model="editForm" :rules="rules" ref="editRuleForm" label-width="100px">
                <el-form-item label="接口名称" prop="name">
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>

                <el-form-item label="接口描述" prop="description">
                    <el-input v-model="editForm.description"></el-input>
                </el-form-item>

                <el-form-item label="接口详情" prop="context">
                    <editor v-model="editForm.context" @init="editorInit" lang="json" theme="chrome" width="450"
                            height="200"></editor>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEditInterface">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {addInterface, deleteInterface, getInterfaces, updateInterface} from "../../request/interface";

    export default {
        name: "index",
        components: {
            // interface页面的context文件框
            editor: require("vue2-ace-editor")
        },
        data() {
            return {
                editDialogVisible: false,
                addDialogVisible: false,
                serviceId: 0,
                interfaces: [],

                addForm: {
                    name: "",
                    description: "",
                    context: "",
                    service_id: ""
                },

                editForm: {
                    service_id: "",
                    id: "",
                    name: "",
                    description: "",
                    context: ""
                },
                rules: {
                    name: [
                        {required: true, message: '请输入接口名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请输入接口描述', trigger: 'blur'},
                    ],
                    context: [
                        {required: true, message: '请输入接口详情', trigger: 'blur'},
                    ]
                },

            }

        },
        methods: {
            // 这个就是在interface页面中的context文本编辑功能
            editorInit: function () {
                require('brace/ext/language_tools') //language extension prerequsite...
                require('brace/mode/json')
                require('brace/mode/javascript')    //language  这里改为json
                require('brace/mode/less')
                require('brace/theme/chrome')
                require('brace/snippets/javascript') //snippet
            },
            saveEditInterface() {
                this.$refs.editRuleForm.validate((valid) => {
                    if (valid) {
                        let req = JSON.parse(JSON.stringify(this.editForm))
                        req.context = JSON.parse(req.context)
                        updateInterface(req.id, req).then(data => {
                            let success = data.data.data
                            if (success) {
                                this.$message({
                                    message: '修改成功',
                                    type: 'success'
                                });
                                this.getInterfacesFun();
                                this.editDialogVisible = false;

                            } else {
                                this.$notify.error({
                                    title: "错误",
                                    message: data.data.error.message
                                });
                            }
                        })

                    } else {
                        console.log("edit submit")
                        return false;
                    }
                })

            },
            saveAddInterface() {
                // 重点学习一下，表单处理
                this.$refs.addRuleForm.validate((valid) => {
                    if (valid) {
                        let req = JSON.parse(JSON.stringify(this.addForm))
                        req.context = JSON.parse(req.context)
                        req.service_id = this.serviceId;
                        addInterface(req).then(data => {
                            let success = data.data.data
                            if (success) {
                                this.$message({
                                    message: '创建成功',
                                    type: 'success'
                                });
                                this.getInterfacesFun();
                                this.addDialogVisible = false;

                            } else {
                                this.$notify.error({
                                    title: "错误",
                                    message: data.data.error.message
                                });
                            }
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });

            },


            openAddModal() {
                let context = {
                    "method": "get",
                    "url": "",
                    "params": {},
                    "asst": {}
                }
                this.addForm.context = JSON.stringify(context, null, 4)
                this.addDialogVisible = true;
            },
            openEditDialog(data) {
                this.editForm.id = data.id;
                this.editForm.name = data.name;
                this.editForm.description = data.description;
                this.editForm.service_id = data.service_id;
                this.editForm.context = JSON.stringify(data.context, null, 4)
                this.editDialogVisible = true;

            },
            getServiceId() {
                //获取url里边的参数
                let serviceId = this.$route.query.serviceId
                if (!serviceId) {
                    this.serviceId = 0
                    return
                }
                this.serviceId = Number(serviceId)
            },

            getInterfacesFun() {
                getInterfaces(this.serviceId).then(data => {
                    let success = data.data.success;
                    if (success) {
                        this.interfaces = data.data.data;
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        });

                    }

                })
            },
            deleteInterfaceFun(interfaceId) {
                this.$confirm('此操作将永久删除该接口, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    //确定删除
                    deleteInterface(interfaceId).then(data => {
                        let success = data.data.success
                        if (success) {
                            this.$message({
                                message: '删除成功',
                                type: 'success'
                            });
                            this.getInterfacesFun()
                        } else {
                            this.$notify.error({
                                title: "错误",
                                message: data.data.error.message
                            })
                        }
                    })
                })

            }

        },
        created() {
            this.getServiceId();
            this.getInterfacesFun()
        },
        watch: {
            "$router.query": function () {
                this.getServiceId();
                this.getInterfacesFun()

            }

        },
    }
</script>

<style scoped>
    .interface_main {
        text-align: left;
        padding: 5px 5px;
    }
</style>