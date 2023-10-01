<template>
    <v-card height="500" width="1200" class="d-flex justify-center align-center">
            <v-chart  class="chart" :option="option" autoresize />
    </v-card>
</template>
<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import {TitleComponent,TooltipComponent,LegendComponent,} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, provide, watch, onBeforeMount  } from 'vue';
import { useAppStore } from '@/store/app'
const piniaStore = useAppStore();
import StoreApi from '@/services/StoreApi';
const chartData = ref({});

/* onBeforeMount(async () => {
  try {
    const res = (await ManagementApi.getChartData());
    if (res.status == 200) {
      chartData.value = res.data;
    } else {
      piniaStore.setSnackBar("Error In Loading Data, Please Contact IT For Support!");
    }
  } catch (error) {
    if (error.message) {
      piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
    } else piniaStore.setSnackBar("Error in getting data. Please Contact IT For Support")
  }
  
  // Initialize chart options based on the fetched data
  option.value.series[0].data = [
    { value: chartData.value.MAPPED_ACCOUNT, name: 'Mapped Account'  },
    { value: chartData.value.TYPE_NEED, name: 'Type Needed' },
    { value: chartData.value.OWMER_NEED, name: 'Owner Needed' },
    { value: chartData.value.EXPIRE_SOON, name: 'Expire Soon' },
  ];
});
 */

use([
CanvasRenderer,
PieChart,
TitleComponent,
TooltipComponent,
LegendComponent,
]);
provide(THEME_KEY, 'dark');
const option = ref(/* {
title: {
text: 'Mapped Account Chart',
left: 'center',
},
tooltip: {
trigger: 'item',
formatter: '{a} <br/>{b} : {c} ({d}%)',
},
legend: {
orient: 'vertical',
left: 'left',
data: ['Mapped Account','Type Needed','Owner Needed','Expire Soon'], //keys
},
series: [
{
name: 'Mapped Account Chart',
type: 'pie',
radius: '65%',
center: ['50%', '60%'],
data: [
{ value: 0, name: 'Mapped Account' },
{ value: 0, name: 'Type Needed' },
{ value: 0, name: 'Owner Needed' },
{ value: 0, name: 'Expire Soon'   },
],
color: ['green', 'yellow', 'red', 'orange'],
animation: true, 
emphasis: {
itemStyle: {
shadowBlur: 10,
shadowOffsetX: 0,
shadowColor: 'rgba(0, 0, 0, 0.5)',
},
},
},
],
} */
{
  title: {
    text: 'Referer of a Website',
    subtext: 'Fake Data',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
});
</script>