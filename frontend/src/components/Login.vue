<template>
    <v-card class="mx-auto mt-16" width="25%" elevation="7"  style="background-color: rgba(255, 255, 255, 0.8);">
        <v-row>
            <v-col cols="1"></v-col>
            <v-col cols="10">      
                <v-card-title class="text-center align-center justify-center"><h1 class="display-1 my-10 ml-4">Login </h1></v-card-title>
                <v-row v-if="errorLogin" class="my-6 mx-8">
                        <v-alert
                        color="error"
                        icon="$error"
                        text="We can't find that username and password. You can select 'Forgot Password' or try again."
                        ></v-alert>
                    </v-row>
                <v-card-text class="mt-10 mx-8 pt-10">                    
                    <v-form ref="loginForm">
                        <v-row>
                        <v-text-field
                        label="Username"
                        prepend-icon="mdi-account-circle"
                        variant="underlined"
                        :rules="[ v => !!v || 'Username is required']"
                        v-model="username"
                        ></v-text-field>
                        </v-row>
                        <v-row class="mb-5">
                        <v-text-field
                        :type="showPassword ? 'text' : 'password'"
                        label="Password"
                        prepend-icon="mdi-lock"
                        append-icon="mdi-eye-off"
                        variant="underlined"                        
                        v-model="password"
                        @click:append="showPassword = !showPassword"></v-text-field>
                        </v-row>
                        <v-card-actions >
                            <v-row class="mt-16 mb-10">
                            <v-btn color="indigo-darken-3" variant="flat" block class="mt-4" :loading="loading" @click="login">
                                Sign In</v-btn>   
                            </v-row>                                              
                        </v-card-actions>
                        <v-row class="mt-8">
                            <v-checkbox
                                v-model="rememberSelected"
                                label="Remember Me"
                                value="remember"
                            ></v-checkbox>
                            <a class="mt-5" @click="ForgotPassword">Forgot Password</a>
                        </v-row>                           
                    </v-form>
                </v-card-text>
            </v-col>
            <v-col cols="1"></v-col>
            <!-- 
            <v-col cols="8">
                <v-img
                    class="bg-white"
                    :aspect-ratio="1"
                    src="@/assets/sushi-bg.jpg"
                    cover
                ></v-img>
            </v-col> -->
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
const errorLogin= ref(false);
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
            console.log(response);
            if(response.status == 200){
                piniaStore.loginSuccess = true;
                if(response.data.role){
                    piniaStore.currentRole = response.data.role;
                }
                piniaStore.currentUserName = username.value;                
                console.log(piniaStore.loginSuccess);
                router.push({name: 'Home'})
            }
        }
        catch(error)
        {
            if(error.response.status === 404 || error.response.status === 401){
                errorLogin.value = true;
            }
            //if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
            else if(error.response.status !== 200) piniaStore.setSnackBar("Error In Assigning Account Owner. Please Contact IT For Support");
        }
        finally{
            loading.value = false;
        }
    }
    else
    {
      piniaStore.setSnackBar("Invalid field(s). Please check your input again !");
    }    
}
function ForgotPassword(){
    router.push({name: 'Login'});
    piniaStore.forgotPW = true;
}
</script>