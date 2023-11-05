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
const chartData = ref([]);

onBeforeMount(async () => {
  try {
    const res = (await StoreApi.getPieChartData());
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
});

use([
CanvasRenderer,
PieChart,
TitleComponent,
TooltipComponent,
LegendComponent,
]);
provide(THEME_KEY, 'dark');
const option = ref(
{
  title: {
    text: 'Number of Supply by Vendor',
    subtext: 'Sushi, Produce and Other',
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
      data: chartData,
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
