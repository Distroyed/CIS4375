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
 const store = useAppStore();
 import { useAppStore } from '@/store/app';
// Check if user data exists in session storage and initialize the store
const currentUserName = (sessionStorage.getItem('currentUserName'));
const currentUser = (sessionStorage.getItem('currentUser'));
const currentRole = (sessionStorage.getItem('currentRole'));
const loginSuccess = (sessionStorage.getItem('loginSuccess'));
if (loginSuccess) {
  store.initializeUserData(currentUserName, currentUser, currentRole, loginSuccess);
}

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