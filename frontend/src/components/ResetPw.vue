<template>
    <v-card class="mx-auto mt-16" width="25%" elevation="7"  style="background-color: rgba(255, 255, 255, 0.8);">
        <v-row class="text-center align-center justify-center" v-if="loading && resetPassword!=1">
            <v-progress-circular
            :size="70"
            :width="7"
            color="green"
            indeterminate
            class="my-10 mx-10"
            ></v-progress-circular>
        </v-row>
        <v-row v-if="!loading && badID && resetPassword!=1">
            <v-alert
                color="error"
                type="error"
                title="Link Error"
                icon="$error"
                text="This link is either expired or wrong, please request a new link to reset password."
            ></v-alert>
        </v-row>
        <div v-if="!loading && !badID && resetPassword==1">
            <v-row>
            <v-alert
                color="success"
                icon="$success"
                title="Password Reset Successfully"
                text="Congratulation, your password has been reset."
                class="mt-8 mx-10"
            ></v-alert>
            </v-row>
            <v-row justify="center" class="mt-6 mb-4">
            <v-card-actions>                
                <v-btn color="green-darken-3" variant="flat" block :loading="submitLoading" @click="back">
                Back To Login</v-btn>    
            </v-card-actions>
            </v-row>
        </div>
        <v-row v-if="!loading && !badID && resetPassword!=1">
        <v-col cols="1"></v-col>
        <v-col cols="10">     
        <v-card-title class="text-center align-center justify-center"><h1 class="display-1 my-10 ml-4">Reset Password </h1></v-card-title>
        <v-card-text>      
            <v-row class="text-center align-center justify-center my-6"> <h3>Please Answer The Security Question And Enter Your New Password</h3></v-row>
            <v-row v-if="resetPassword==0">
            <v-alert
                color="error"
                icon="$error"
                text="Your answer is incorrect, please retry again."
                class="mb-5"
            ></v-alert>
            </v-row>
            <v-form ref="resetPwForm">
                <v-row>
                    <p><span style="font-weight: bold;">Security Question: </span>{{ accountData.sec_question }}</p>
                </v-row>
                <v-row>                    
                    <v-text-field
                        v-model="accountData.sec_response"
                        label="Security question answer"
                        color="primary"
                        :rules="[ v => !!v || 'Answer is required']"
                        variant="underlined"></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="accountData.password"
                        label="Password"
                        type="password"
                        color="primary"
                        :rules="[ v => !!v && v.length >= 6 || 'Password must be at least 6 characters']"
                        variant="underlined"></v-text-field>
                </v-row>    
                <v-row>
                    <v-text-field
                        v-model="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        color="primary"
                        :rules="[ v => !!v || 'Password is required']"
                        variant="underlined"></v-text-field>
                </v-row> 
                <v-row class="mx-7 mb-4">
                    <v-alert density="compact" type="error" v-if="passwordsDoNotMatch">
                        Passwords do not match
                    </v-alert>
                </v-row>
                <v-card-actions>
                        <v-row justify="center">
                        <v-btn color="indigo-darken-3" variant="flat" block :loading="submitLoading" @click="submit">
                        Submit</v-btn>    
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
const router = useRouter();
const route = useRoute();
const linkID = route.params.id;
const badID = ref(false);
const piniaStore = useAppStore();
const confirmPassword = ref(null)
const submitLoading =ref(false);
const resetPwForm = ref(null);
const passwordsDoNotMatch = computed(() => accountData.value.password !== confirmPassword.value)

//Verify the reset password id
const loading = ref(false);
const accountData = ref({});
onBeforeMount( async () =>{
    try{
        loading.value = true;
        //Send link ID to backend to verify
        //console.log(linkID);
        const res = await StoreApi.verifyLink(linkID);
        if(res.status === 200){
            accountData.value = res.data
            badID.value = false;
        }
        else if(res.status === 205){
            badID.value = true;
            piniaStore.setSnackBar("Link Is Expired!")
        }
    }
    catch(error)
    {
        badID.value = true;
        if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
        else piniaStore.setSnackBar("Error In Loading Page. Please Contact IT For Support");        
    }
    finally{
        loading.value = false;
    }
});

//Submit Reset Password Request
const resetPassword = ref(-1);
async function submit(){
    const {valid} = await resetPwForm.value.validate();
    if(valid && !passwordsDoNotMatch.value)
    {
        try{
            loading.value = true;
            accountData.value.link_id = linkID;
            //console.log(accountData.value);
            
            const res = await StoreApi.resetPassword(accountData.value);
            if(res.status === 200){
                piniaStore.setSnackBar("Password Updated Successfully", true);
                resetPassword.value = 1;
            }
            else if(res.status === 205){
                resetPassword.value = 0;
                piniaStore.setSnackBar("Wrong Answer");
            }            
        }
        catch(error)
        {
            if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
            else piniaStore.setSnackBar("Error In Finding Account. Please Contact IT For Support");
        }
        finally{
            loading.value = false
        }
    }
}

function back(){
    router.push({name: 'Login'});
}
</script>
