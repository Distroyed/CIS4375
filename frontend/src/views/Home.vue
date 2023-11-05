<template>
  <v-container fluid>
      <v-responsive class="d-flex justify-center align-center text-center fill-height">
          <Transition name="fade" mode="out-in">
              <v-row class="pa-3 justify-center align-center d-flex">
              <!-- <v-col cols="auto">
                  <v-btn
                  variant="plain"
                  size="large"
                  icon="mdi-chevron-left"
                  @click="goNext()"
                  ></v-btn>
              </v-col> -->
              <v-col cols="auto">
                  <component :is="selectedChartComponent"></component>
              </v-col>
              <!-- <v-col cols="auto">
                  <v-btn
                  size="large"
                  variant="plain"
                  icon="mdi-chevron-right"
                  @click="goBack()"
                  ></v-btn>
              </v-col> -->
              </v-row>
          </Transition>
      </v-responsive>
      <v-row class="align-center d-flex justify-center pt-2">
      <template  v-for="(item, i) in views">
          <v-col cols="auto" class="mx-5">
              <v-hover v-slot="{ isHovering, props }">
                  <v-card
                  :elevation="isHovering ? 12 : 2"
                  :class="{ 'on-hover': isHovering }"
                  class="card-tab mx-auto"
                  :color="item.color"
                  width="350"
                  height="200"
                  max-width="400"
                  theme="dark"
                  v-bind="props"
              >
                  <v-card-title class="text-h5 text-center">
                      <v-icon :icon="item.icon" size="large"></v-icon>
                      {{ item.title }}
                  </v-card-title>
                  <p style="text-align:center">{{ item.desc }}</p>
                  <v-card-actions justify="center">
                      <v-btn
                          class="mt-8"
                          block rounded
                          variant="outlined"
                          size="small"
                          prepend-icon="mdi-check"
                          @click="switchViews(i)"
                      >
                      {{ item.buttonLabel }}
                      </v-btn>
                  </v-card-actions>
              </v-card>
              </v-hover>                
          </v-col>
      </template>    
</v-row>
  </v-container>
</template>
<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/store/app';
const piniaStore = useAppStore();
const router = useRouter();
const views = ref([
  {title : 'Supply', icon : 'mdi-apps-box', desc : 'View and Manage Supply.', color : '#1E88E5', buttonLabel :'Get Started'},
  {title : 'Vendor', icon : 'mdi-store-outline', desc : 'View and Manage Vendor.', color : '#43A047', buttonLabel :'Get Started'},
  {title : 'Account', icon : 'mdi-account-box-outline', desc : 'View and Manage Account.', color : '#E53935', buttonLabel :'Get Started'},
  {title : 'Order', icon : 'mdi-clipboard-list-outline', desc : 'Order Supply.', color : '#5E35B1', buttonLabel :'Get Started'}
]);
async function switchViews(id){
  switch(id){
      case 0:
          router.push({name : 'Supply'});
          break;
      case 1:
          router.push({name : 'Vendor'});
          break;
      case 2:
        if(piniaStore.currentRole === 'admin'){
            router.push({name : 'Account'});
            break;
        }
        else{
            piniaStore.setSnackBar("You're not allowed to access this page!");
            break;
        }          
      case 3:
          router.push({name : 'Order'});
          break;
      default:
          {break;}
  }
}
import { defineAsyncComponent } from 'vue'
const componentMap = {
PieMappedChart: defineAsyncComponent(() =>
  import('@/components/PieMappedChart.vue'),
)
}
const chartComponents = Object.keys(componentMap);
const selectedChartIndex= ref(0);
const selectedChartComponent = computed(() => {
  return componentMap[chartComponents[selectedChartIndex.value]];
});
</script>
<style scoped>
.card-tab {
  transition: opacity .4s ease-in-out;
}

.card-tab:not(.on-hover) {
  opacity: 0.6;
}
</style>
