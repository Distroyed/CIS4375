<template>
  <nav>
    <v-snackbar
      v-model="store.showSnackBar"
      :timeout="4000"
      location="top"
      :color="store.isSuccess ? 'green':'deep-orange-darken-3' "
      elevation="24"
      multi-line
    >
    <p class="text-subtitle-2 text-center">{{store.catchError}}</p>
    </v-snackbar>
    <v-app-bar 
      :elevation="1" 
      color="blue-darken-1"
      dark
      density="comfortable"
    >
    <template v-slot:prepend>
        <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
      <span class="mdi mdi-security ml-2 text-h6" @click="goHome()"></span>
    <v-app-bar-title @click="goHome()">
        <span class="text-overline"
        >7 Friday
        <span class="text-red">
        Sushi
        </span> - <span class="font-weight-bold">Food Inventory Application </span></span> 
    </v-app-bar-title>
    <span class="text-button mr-4" v-if="loginSuccess && currentUserName">Welcome, {{ currentUser }}</span>
<!-- <span class="text-button mr-4">{{ piniaStore.username }}</span> -->
    </v-app-bar>
        <v-navigation-drawer
          v-model="drawer"
          location="left"
          temporary
          v-if="piniaStore.loginSuccess"
        >
        <v-list nav>
            <v-list-item
              v-for = "(item, i) in menuItems"
              :key="i"
              :value="item"
              color="primary"
              @click="selectedMenuItem(item)"           
            >
              <template v-slot:prepend>
                <v-icon :icon="item.icon"></v-icon>
              </template>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item>
        </v-list>
        </v-navigation-drawer>
  </nav>
</template>

<script setup>
import { useAppStore } from '@/store/app';
const store = useAppStore();
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const piniaStore = useAppStore();

//retrieve data from session storage
const loginSuccess = sessionStorage.getItem('loginSuccess');
const currentUserName = sessionStorage.getItem('currentUserName');
const currentRole = sessionStorage.getItem('currentRole');
const currentUser = sessionStorage.getItem('currentUser');

const drawer = ref(false);
const menuItems = ref([
  {title : 'Home', icon : 'mdi-home'},  
  {title : 'Supply', icon : 'mdi-apps-box'},
  {title : 'Vendor', icon : 'mdi-store-outline'},
  {title : 'Account', icon : 'mdi-account-box-outline'},
  {title : 'Order', icon : 'mdi-clipboard-list-outline'},
  {title : 'LogOut', icon : 'mdi-logout'},
]);
//Function to handle menu item selection
async function selectedMenuItem(item){
  switch(item.title)
  {
    case 'Home':
      router.push({name: 'Home'});
      break;
    case 'Supply':
      router.push({name: 'Supply'});
      break;
    case 'Vendor':
      router.push({name: 'Vendor'});
      break;
    case 'Account':
      if(currentRole === 'admin'){
        router.push({name: 'Account'});
        break;
      }
      else{
        piniaStore.setSnackBar("You are not allowed to access this page!")
        break;
      }
    case 'Order':
      router.push({name: 'Order'});
      break;
    case 'LogOut':
      piniaStore.loginSuccess = false;
      piniaStore.currentRole='';
      piniaStore.currentUser='';
      piniaStore.currentUserName='';
      piniaStore.clearAuthenticationStatus();

      router.push({name: 'Login'});
      break;
    default:
      break;
  }
}
</script>
