<template>
  <v-app style="background-color: white;">
    <NavBar />
    <router-view v-slot="{Component}">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>   
  </v-app>
</template>


<script setup>
 import NavBar from './components/NavBar'


 </script>

<style>

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>