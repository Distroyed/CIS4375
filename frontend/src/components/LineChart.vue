<template>
  <v-card height="500" width="1200" class="d-flex justify-center align-center">
          <v-chart  class="chart" :option="option" autoresize />
  </v-card>

</template>
<script setup>
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import {
GridComponent,
TitleComponent,
TooltipComponent,
LegendComponent,
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, provide } from 'vue';

use([
CanvasRenderer,
LineChart,
GridComponent,
TitleComponent,
//TooltipComponent,
//LegendComponent,
]);
provide(THEME_KEY, 'dark');

const option = ref({
  xAxis: {
  data: ['A', 'B', 'C', 'D', 'E']
},
yAxis: {},
series: [
  {
    data: [10, 22, 28, 23, 19],
    type: 'line',
    lineStyle: {
        color: 'white',
        width: 4,
        type: 'line'
    }
  }
]
});

</script>