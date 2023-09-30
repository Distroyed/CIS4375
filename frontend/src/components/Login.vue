<template>
    <v-card class="mx-auto mt-16" width="80%" height="80%" elevation="7">
        <v-row>
            <v-col cols="5">      
                <v-card-title><h1 class="display-1 my-10 ml-4">Sign In </h1></v-card-title>
                <v-card-text class="mt-10 mx-8">
                    <v-form ref="loginForm">
                        <v-text-field
                        label="Username"
                        prepend-icon="mdi-account-circle"
                        variant="underlined"
                        :rules="[ v => !!v || 'Username is required']"
                        v-model="username"
                        ></v-text-field>
                        <v-text-field
                        :type="showPassword ? 'text' : 'password'"
                        label="Password"
                        prepend-icon="mdi-lock"
                        append-icon="mdi-eye-off"
                        variant="underlined"
                        
                        v-model="password"
                        @click:append="showPassword = !showPassword"></v-text-field>
                        <v-card-actions>
                            <v-btn color="indigo-darken-3" variant="flat" block class="mt-4" :loading="loading" @click="login">
                                Sign In</v-btn>                                                 
                        </v-card-actions>
                        <v-row class="mt-2">
                            <v-checkbox
                                v-model="rememberSelected"
                                label="Remember Me"
                                value="remember"
                            ></v-checkbox>
                            <a class="mt-5">Forgot Password</a>
                        </v-row>                           
                    </v-form>
                </v-card-text>
            </v-col>
            <v-col cols="7">
                <v-img
                    class="bg-white"
                    :aspect-ratio="1"
                    src="@/assets/sushi-bg.jpg"
                    cover
                ></v-img>
            </v-col>
        </v-row>
    </v-card>
    
</template>
<script setup>
//:rules="passwordRule"
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import StoreApi from '@/services/StoreApi';
const piniaStore = useAppStore();
const router = useRouter();
const showPassword = ref(false);
const rememberSelected = ref(false);
const username = ref();
const password = ref();
const loading = ref(false);
const loginForm=ref(null);
const storeUsername = piniaStore.username;
const storePassword = piniaStore.password;
const passwordRule = [
  value => {
    // Check for empty value
    if (!value) return 'This field is required';

    // Check for at least 8 characters
    if (value.length < 8) return 'Must have at least 8 characters';

    // Check for at least 1 special character, 1 uppercase, and 1 number
    const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]/.test(value);
    const hasUppercase = /[A-Z]/.test(value);
    const hasNumber = /\d/.test(value);

    if (!hasSpecialChar || !hasUppercase || !hasNumber) {
      return 'Must contain at least 1 special character, 1 uppercase letter, and 1 number';
    }

    return true; // Validation passed
  },
];
async function login(){
    const {valid} = await loginForm.value.validate();
    if(valid)
    {
        loading.value = true;
        try{
            const credentials = 
            {   username: username.value,
                password: password.value };
            const response = await StoreApi.login(credentials);
            if(response.status == 200){
                console.log(response.data)
                piniaStore.loginSuccess = true;
                //piniaStore.currentUser = response.data;
                //piniaStore.currentRole = response.data;
                router.push({name: 'Home'})
            }
            /* if(username.value.trim().toUpperCase() === storeUsername.trim().toUpperCase() 
            && password.value.trim().toUpperCase() === storePassword.trim().toUpperCase())
            {
                piniaStore.loginSuccess = true;
                router.push({name: 'Home'})
            }
            else{
                piniaStore.setSnackBar("Username or Password doesn't match!!!");
            } */
        }
        catch(error)
        {
            if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
                else piniaStore.setSnackBar("Error In Assigning Account Owner. Please Contact IT For Support");
        }
    }
    else
    {
      piniaStore.setSnackBar("Invalid field(s). Please check your input again !");
    }
    
}
</script>