<template>
    <div class="main-list">
        <!--        <div class="service-list">-->
        <!--            <div v-for="item in serviceList" :key="item.id" class="service-item">-->
        <!--                                <a href="javascript:void(0)" style='text-decoration:none;'-->
        <!--                                   @click="getInterfacesFun(item.id)">-->
        <!--                                    {{item.name}}-->

        <!--                                </a>-->
        <!--            </div>-->

        <!--        </div>-->
        <div class="interface-list">
            <el-select v-model="serviceId" placeholder="请选择" @change="changeSelectService">
                <el-option
                        v-for="item in serviceList"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id">
                </el-option>
            </el-select>
            <el-table
                    @selection-change="handleSelectionChange"
                    :data="interfaceList"
                    stripe
                    style="width: 100%;max-height: 600px; overflow: auto">
                <el-table-column
                        type="selection"
                        width="%5">
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="名称"
                        min-width="45%">
                </el-table-column>
                <el-table-column
                        label="URL"
                        min-width="50%">
                    <template slot-scope="scope">
                        {{scope.row.context.url}}
                    </template>
                </el-table-column>
            </el-table>

        </div>
    </div>
</template>

<script>
    import {getAllService} from "../../request/service";
    import {getInterfaces} from "../../request/interface";


    export default {
        name: "selectInterface",
        data() {
            return {
                serviceId: undefined,
                serviceList: [],
                interfaceList: [],
                multipleSelection: [],
                servicePageSize: undefined, //默认展示10条服务
            }
        },
        methods: {
            changeSelectService(serviceId) {
                this.getInterfacesFun(serviceId)

            },
            handleSelectionChange(val) { // 已选择框的回调，把已选择的所有数据返回出来
                this.multipleSelection = val;

            },
            getInterfacesFun(serviceId) {
                getInterfaces(serviceId).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.interfaceList = data.data.data;
                    } else {
                        this.$notify.error({
                            title: "错误",
                            message: data.data.error.message
                        })
                    }
                })
            },
            // 最笨办法，多请求一次，只为获取服务列表总数
            getAllServiceFun() {
                getAllService(1, 1).then(data => {
                    let success = data.data.success
                    if (success) {
                        this.servicePageSize = data.data.count;
                        getAllService(1, this.servicePageSize).then(data => {
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
                    } else {
                        this.$notify.error({
                            title: "获取服务列表失败",
                            message: data.data.error.message
                        })
                    }
                })

            },
        },
        created() {
            this.getAllServiceFun();
        },

    }
</script>

<style scoped>
    .main-list {
        display: flex;
    }

    .service-list {
        width: 20%;
        padding: 5px;

    }

    .interface-list {
        width: 100%;
        padding: 5px;

    }

    .service-item {
        font-size: 18px;
        padding: 10px 0 5px 5px;
    }
</style>