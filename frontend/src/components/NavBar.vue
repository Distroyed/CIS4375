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
<!--     <span class="text-button mr-4">{{ winUser }}</span> -->
    </v-app-bar>
        <v-navigation-drawer
          v-model="drawer"
          location="left"
          temporary
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
import { useAppStore } from '@/store/app'
const store = useAppStore()
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const piniaStore = useAppStore();
const drawer = ref(false);
const menuItems = ref([
  {title : 'Home', icon : 'mdi-home'},
  {title : 'LogOut', icon : 'mdi-logout'},
]);
//Function to handle menu item selection
async function selectedMenuItem(item){
  switch(item.title)
  {
    case 'Home':
      router.push({name: 'Home'});
      break;
    case 'LogOut':
      piniaStore.loginSuccess = false;
      router.push({name: 'Login'});
      break;
    default:
      break;
  }
}
async function goHome(){
  router.push({name: 'Home'});
}
</script>
