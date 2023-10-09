<template>
  <v-app class="background-image">
    <v-container class="my-10 pa-10" fluid fill-height>
      <v-responsive class="d-flex fill-height ma-5 pa-5 " > 
        <ResetPw />
      </v-responsive>
    </v-container>   
  </v-app> 
</template>
  
  <script setup>
    import ResetPw from '@/components/ResetPw.vue'
  </script>
  <style>
  .background-image {
    background-image: url('@/assets/bg3.jpg'); 
    background-size: cover;
    background-repeat: no-repeat;
  }
  </style>
  