<template>
    <div>
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
                    {{scope.row.context.url}}
                </template>
            </el-table-column>

            <el-table-column label="操作" width="200">
                <template>
                    <el-button
                            size="mini">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import {getAllInterfaces} from "../../request/interface";

    export default {
        name: "index",
        data() {
            return {
                serviceId: 0,
                interfaces: []
            }

        },
        methods: {
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
                getAllInterfaces(this.serviceId).then(data => {
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

</style>