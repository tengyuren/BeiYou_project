<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-pie-chart"></i> 各类业务图表
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
<!--            <div class="plugins-tips">
                vue-schart：vue.js封装sChart.js的图表组件。
                访问地址：
                <a href="https://github.com/lin-xin/vue-schart" target="_blank">vue-schart</a>
            </div>-->
            <div class="schart-box">
                <div class="content-title">电话业务随机特性柱状图</div>
                <schart class="schart" canvasId="bar" :options="options1"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">电话业务随机特性折线图</div>
                <schart class="schart" canvasId="line" :options="options2"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">P2P业务分配饼状图</div>
                <schart class="schart" canvasId="pie" :options="options3"></schart>
            </div>
            <div class="schart-box">
                <div class="content-title">固定互联网宽带接入速率</div>
                <schart class="schart" canvasId="ring" :options="options4"></schart>
            </div>
        </div>
    </div>
</template>

<script>
import Schart from "vue-schart";
export default {
    name: "basecharts",
    components: {
        Schart,
    },
    setup(){
        const options1 = {
            type: "bar",
            title: {
                text: "电话业务随机特性",
            },
            bgColor: "#fbfbfb",
          labels: ["0", "4","6", "8","10", "12", "14","16","18","20","22","24"],
          datasets: [
            {
              label: "普通电话呼叫的随机特性",
              data: [0, 1,5, 40, 100,60,55, 60,45,30,10,0],
            },
            {
              label: "拨号上网请求的随机特性",
              data: [170,50,30,60,160,175,170,172,183,240,250,115],
            }
            ],
        };
        const options2 = {
            type: "line",
            title: {
                text: "电话业务的随机特性",
            },
            bgColor: "#fbfbfb",
            labels: ["0", "4","6", "8","10", "12", "14","16","18","20","22","24"],
            datasets: [
                {
                    label: "普通电话呼叫的随机特性",
                    data: [0, 1,5, 40, 100,60,55, 60,45,30,10,0],
                },
                {
                    label: "拨号上网请求的随机特性",
                    data: [170,50,30,60,160,175,170,172,183,240,250,115],
                }
            ],
        };
        const options3 = {
            type: "pie",
            title: {
                text: "P2P业务分配",
            },
            legend: {
                position: "left",
            },
            bgColor: "#fbfbfb",
            labels: [
                "Audio",
                "Video",
                "Others",

            ],
            datasets: [
                {
                    data: [11,61,27],
                },
            ],
        };
        const options4 = {
            type: "ring",
            title: {
                text: "固定互联网宽带接入速率",
            },
            showValue: false,
            legend: {
                position: "bottom",
                bottom: 40,
            },
            bgColor: "#fbfbfb",
            labels: ["1000M以上", "20M以下", "20M-100M之间","100M-1000M"],
            datasets: [
                {
                    data: [0.2, 1.8, 12.8,85.2],
                },
            ],
        };
        return {
            options1,
            options2,
            options3,
            options4,
        };
    },
}
</script>

<style scoped>
.schart-box {
    display: inline-block;
    margin: 20px;
}
.schart {
    width: 600px;
    height: 400px;
}
.content-title {
    clear: both;
    font-weight: 400;
    line-height: 50px;
    margin: 10px 0;
    font-size: 22px;
    color: #1f2f3d;
}
</style>