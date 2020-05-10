<template>
    <div>
        interface
    </div>
</template>

<script>
    export default {
        name: "index",
        data(){
            return {
                serviceId: 0,
            }

        },
        methods: {
            getServiceId(){
                //获取url里边的参数
                let serviceId = this.$router.query.serviceId
                if (!serviceId){
                    this.serviceId = 0
                    return
                }
                this.serviceId = Number(serviceId)
            }

        },
        created() {
            this.getServiceId()
        },
        watch: {
            "$router.query": function () {

            }

        },
    }
</script>

<style scoped>

</style>