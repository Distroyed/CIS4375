<template>
  <v-app class="background-image">
    <v-container class="my-10 pa-10" fluid fill-height>
      <v-responsive class="d-flex fill-height ma-5 pa-5 " >
        <div v-if="piniaStore.forgotPW"> <ForgotPassword /></div>
        <div v-else><Login /></div>
      </v-responsive>
    </v-container>   
  </v-app> 
</template>
  
  <script setup>
    import Login from '@/components/Login.vue'
    import ForgotPassword from '@/components/ForgotPassword.vue'
    import { useAppStore } from '@/store/app'
    const piniaStore = useAppStore();
  </script>
  <style>
  .background-image {
    background-image: url('@/assets/bg3.jpg'); 
    background-size: cover;
    background-repeat: no-repeat;
  }
  </style>
  