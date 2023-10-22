<template>
    <v-card class="mx-auto mt-16" width="25%" elevation="7"  style="background-color: rgba(255, 255, 255, 0.8);">
        <v-row>
        <v-col cols="1"></v-col>
        <v-col cols="10">     
        <v-card-title class="text-center align-center justify-center"><h1 class="display-1 my-10 ml-4">Forgot Password </h1></v-card-title>
        <v-card-text>      
            <v-row justify="center" class="my-4" v-if="!resetPW"> <h3>Please Enter Your Email Address</h3></v-row>       
            <v-row v-if="errorEmail" class="my-6 mx-8">
                <v-alert
                color="error"
                icon="$error"
                text="We can't find the account associated with your email, please enter a different email."
                ></v-alert>
            </v-row>       
            <v-form ref="forgotPWForm">
                <v-row class="my-4" v-if="!resetPW">
                    <v-text-field
                    label="Email"
                    prepend-icon="mdi-account-circle"
                    variant="underlined"
                    :rules="emailRule"
                    class="mx-9"
                    v-model="email"
                    ></v-text-field>
                </v-row>    
                <v-row class="my-4" v-if="resetPW">
                    <v-alert
                        type="success"
                        title="Reset Password Email Sent"
                        text="An email has been sent to your email address, please follow instruction on the email to reset your password. Thank you."
                    ></v-alert>
                </v-row>      
                    <v-card-actions>
                        <v-row justify="center">
                        <v-btn color="indigo-darken-3" width="150" variant="flat"  :loading="loading" @click="submit" v-if="!resetPW">
                        Submit</v-btn>                           
                        <v-btn  color="red-darken-3" width="150" variant="flat"  @click="back">
                        Back</v-btn>
                    </v-row>
                    </v-card-actions>
            </v-form>
        </v-card-text>
        </v-col>
        <v-col cols="1"></v-col>
        </v-row>
    </v-card>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import StoreApi from '@/services/StoreApi';
const piniaStore = useAppStore();
const router = useRouter();
const email = ref(null);
const loading =ref(false);
const forgotPWForm = ref(null);
const errorEmail = ref(false);
const resetPW = ref(false);
const emailRule = [
    v => !!v || 'Field is required',
    value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Invalid Email Format'
    }
];
async function submit(){
    const {valid} = await forgotPWForm.value.validate();
    if(valid)
    {
        try{
            console.log(email.value);
            //errorEmail.value = true;
            // const res = await StoreApi.forgotPassword(email.value)
            resetPW.value = true;
        }
        catch(error)
        {
            if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
            else piniaStore.setSnackBar("Error In Finding Account. Please Contact IT For Support");
        }
    }
}
async function back(){
    router.push({name: 'Login'});
    piniaStore.forgotPW = false;
}
</script>