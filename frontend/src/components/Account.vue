<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
        <v-row class="justify-center align-center text-center">
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Admin Users</v-card-title>
                <span class="text-orange-darken-1 text-h4 font-weight-light">{{ adminCount }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Edit Users</v-card-title>
                <span class="text-red-darken-1 text-h4 font-weight-light">{{ editCount }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">View User</v-card-title>
                <span class="text-purple-darken-1 text-h4 font-weight-light">{{ viewCount }}</span>
            </v-card>
        </v-col>
    </v-row>
        <v-card class="mt-10">
    <v-data-table
        :items-per-page="itemsPerPage"
        item-value="account_id"
        :headers="headers"
        :loading="loading"
        :search="search"
        :items="displayItems"
        density="compact"
        fixed-header
        class="elevation-5">
        <!-- Toolbar group -->
        <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title >Account Management</v-toolbar-title> 
                    <v-divider
                            inset
                            vertical
                            class="mx-5"
                    ></v-divider>   
                    <v-btn
                            variant="flat"
                            color="green"
                            prepend-icon="mdi-plus"
                            size="small"
                            @click="addOrEditAccount()"
                            >
                                Add Account
                            </v-btn>
                    <v-spacer></v-spacer>
                    <v-spacer></v-spacer>
                    <v-btn
                            variant="flat"
                            color="indigo"
                            prepend-icon="mdi-microsoft-excel"
                            size="small"
                            @click="exportCSV()"
                            >
                                Export Csv
                            </v-btn>
                    <v-col cols="3">
                    <v-text-field
                        prepend-icon="mdi-magnify"
                        v-model="search"
                        label="Search Any"
                        class="mr-2 pt-2"
                        variant="underlined"
                        clearable
                    ></v-text-field>
                    </v-col>
                </v-toolbar>
        </template>
        <!-- Action Column -->
        <template v-slot:item.Action="{ item }">
            <v-icon
                class="me-2"
                color="green"
                icon="mdi-pencil"
                size="small"
                :disabled="loading"
                @click="addOrEditAccount(item)">
            </v-icon>   
            <v-icon
                class="me-2"
                color="red"
                icon="mdi-trash-can"
                size="small"
                @click="deleteAccount(item)"
                :disabled="loading">
            </v-icon>  
        </template>          
        </v-data-table>
        <!-- Add Account Dialog -->
        <v-dialog v-model="addOrEditDialog" persistent width="60%">
            <v-card>
                <v-alert
                    type="info"
                    title="Account Role"   
                    closable                 
                    variant="tonal"
                >
                <ol>
                    <li><span style="font-weight: bold;">Admin:</span> High Privileges. Can view, edit and delete all categories including Account, Vendor, Supply,...</li>
                    <li><span style="font-weight: bold;">Edit:</span> Medium Privileges. Can view, edit and delete all categories except for Account</li>
                    <li><span style="font-weight: bold;">View:</span> Lowest Privileges. Can only view certain categories like Vendor, Supply,...</li>
                </ol>
                </v-alert>
                <v-row class="mt-4 justify-center align-center">
                        <v-card-title v-if="isAdd === 1">
                            Add New Account</v-card-title>
                        <v-card-title v-if="isAdd === 0">
                            Edit Current Account</v-card-title></v-row>                    
                    <v-card-text>
                        <v-form ref="addOrEditForm">
                            <v-row class="mx-6 justify-center align-center">
                                <!-- <v-col cols="4">
                                    <v-text-field
                                    v-model="accountItem.username"
                                    label="Account Name"
                                    color="primary"
                                    :rules="[ v => !!v || 'Account Name is required']"
                                    variant="underlined"></v-text-field>
                                </v-col> -->
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="accountItem.username"
                                    label="Email - Username"
                                    color="primary"
                                    type="email"
                                    :rules="emailRule"
                                    placeholder="johndoe@gmail.com"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="accountItem.fname"
                                    label="First Name"
                                    color="primary"
                                    :rules="[ v => !!v || 'First Name is required']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="accountItem.lname"
                                    label="Last Name"
                                    color="primary"
                                    :rules="[ v => !!v || 'Last Name is required']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                            </v-row>                            
                            <v-row class="mx-6">                                
                                <v-col cols="6">
                                    <v-text-field
                                    v-model="accountItem.phone"
                                    label="Phone"
                                    color="primary"
                                    :rules="phoneRule"
                                    type="tel"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="6">
                                    <v-autocomplete
                                    v-model="accountItem.role"
                                    label="Role"
                                    color="primary"
                                    :rules="[ v => !!v || 'Role is required']"
                                    clearable
                                    :items="['admin', 'edit', 'view']"
                                    variant="underlined"></v-autocomplete>
                                </v-col>
                            </v-row>    
                            <v-row class="mx-6">       
                                <v-col cols="6">
                                    <v-autocomplete
                                    v-model="accountItem.sec_question"
                                    label="Security Question"
                                    color="primary"
                                    :rules="[ v => !!v || 'Security Question is required']"
                                    clearable
                                    :items="securityQuestions"
                                    variant="underlined"></v-autocomplete>
                                </v-col>
                                <v-col cols="6">
                                    <v-text-field
                                    v-model="accountItem.sec_response"
                                    label="Security Answer"
                                    color="primary"
                                    :rules="[ v => !!v && v.length >= 3 || 'Answer must be at least 3 characters']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                            </v-row> 
                            <div v-if="isAdd === 1">
                                <v-row class="mx-6">
                                    <v-col cols="6">
                                        <v-text-field
                                        v-model="accountItem.password"
                                        label="Password"
                                        type="password"
                                        color="primary"
                                        :rules="[ v => !!v && v.length >= 6 || 'Password must be at least 6 characters']"
                                        variant="underlined"></v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-text-field
                                        v-model="repeatPassword"
                                        label="Confirm Password"
                                        type="password"
                                        color="primary"
                                        :rules="[ v => !!v && v.length >= 6 || 'Password must be at least 6 characters']"
                                        variant="underlined"></v-text-field>
                                    </v-col>                                    
                                </v-row>
                                <v-row class="mx-7 mb-4">
                                    <v-alert density="compact" type="error" v-if="passwordsDoNotMatch">
                                        Passwords do not match
                                    </v-alert>
                                </v-row>
                            </div>  
                            <v-row class="mx-6" v-if="isAdd===0">
                                <v-checkbox
                                    v-model="resetPw"
                                    label="Reset Password"
                                    value = true
                                    ></v-checkbox>
                            </v-row>  
                            <div v-if="isAdd === 0 && resetPw ==='true'">
                                <v-row class="mx-6">
                                    <v-col cols="6">
                                        <v-text-field
                                        v-model="accountItem.password"
                                        label="Password"
                                        type="password"
                                        color="primary"
                                        :rules="[ v => !!v && v.length >= 6 || 'Password must be at least 6 characters']"
                                        variant="underlined"></v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-text-field
                                        v-model="repeatPassword"
                                        label="Confirm Password"
                                        type="password"
                                        color="primary"
                                        :rules="[ v => !!v && v.length >= 6 || 'Password must be at least 6 characters']"
                                        variant="underlined"></v-text-field>
                                    </v-col>                                    
                                </v-row>
                                <v-row class="mx-7 mb-4">
                                    <v-alert density="compact" type="error" v-if="passwordsDoNotMatch">
                                        Passwords do not match
                                    </v-alert>
                                </v-row>
                            </div>                      
                        </v-form>
                            <v-row justify="center">
                                <v-card-actions>
                                    <v-btn
                                    variant="flat"
                                    color="green"
                                    width="150"
                                    @click.prevent="submitAddOrEdit()"
                                    :disabled="resetPw && passwordsDoNotMatch"
                                    :loading="addOrEditLoading"
                                    prepend-icon="mdi-content-save-outline">
                                    Save
                                    </v-btn>
                                    <v-btn
                                    variant="flat"
                                    width="150"
                                    color="red-lighten-2"
                                    @click.prevent="closeAddOrEdit()" 
                                    prepend-icon="mdi-cancel"
                                    >
                                    Cancel</v-btn>
                                </v-card-actions>
                            </v-row>
                        </v-card-text>
            </v-card>
        </v-dialog>
        <!-- Delete Account Dialog -->
        <v-dialog v-model="delDialog" persistent width="60%">
            <v-card>
                <v-row class="mt-4 justify-center align-center">
                    <v-card-title>
                        Delete Account Confirmation</v-card-title>
                </v-row>                    
                <v-card-text>
                    <v-row justify="center"><h3>Are you sure you want to delete the following account?</h3></v-row>
                    <v-row class="mx-10">
                        <ul>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Username:</span> {{ delAccount.username }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">First Name:</span> {{ delAccount.fname }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Last Name:</span> {{ delAccount.lname }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Phone:</span> {{ delAccount.phone }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Role:</span> {{ delAccount.role }} </p></li>
                        </ul>    
                    </v-row>
                    <v-row justify="center">
                        <v-card-actions>
                                    <v-btn
                                    variant="flat"
                                    color="green"
                                    width="150"
                                    @click.prevent="submitDel()"
                                    :loading="addOrEditLoading"
                                    prepend-icon="mdi-content-save-outline">
                                    Save
                                    </v-btn>
                                    <v-btn
                                    variant="flat"
                                    width="150"
                                    color="red-lighten-2"
                                    @click.prevent="delDialog = false" 
                                    prepend-icon="mdi-cancel"
                                    >
                                    Cancel</v-btn>
                        </v-card-actions>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>
        </v-card>
    </v-container>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import StoreApi from '@/services/StoreApi';
const search = ref(null);
const loading = ref(false)
const itemsPerPage = ref(25);
const piniaStore = useAppStore();
//retrieve data from session storage
const loginSuccess = sessionStorage.getItem('loginSuccess');
const currentUserName = sessionStorage.getItem('currentUserName');
const currentRole = sessionStorage.getItem('currentRole');

const headers = ref([
    { title: 'Action', align: 'center', key: 'Action'},
    { title: 'Username', align: 'left', key: 'username'  },
    { title: 'First Name', align: 'left', key: 'fname'  },
    { title: 'Last Name', align: 'left', key: 'lname'  },
    //{ title: 'Email', align: 'left', key: 'email'  },
    { title: 'Phone', align: 'left', key: 'phone'},
    { title: 'Role', align: 'left', key: 'role' },
    { title: 'Added By', align: 'left', key: 'added_by' },    
    { title: 'Date Added', align: 'left', key: 'date_added' },
    { title: 'Modified By', align: 'left', key: 'modified_by' },    
    { title: 'Modify Date', align: 'left', key: 'date_modified' }
]);
const displayItems = ref([]);
//Fetch Data to Account
onBeforeMount(async () => {
    try{
        const res = await StoreApi.getAccount();
        if(res.status === 200){
            displayItems.value = [...res.data];
        }
    }
    catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ".Please contact IT for support");
        }
        else piniaStore.setSnackBar("Error in getting Account Data. Please contact IT for support");
    }
});

const adminCount = computed(() => {
    return displayItems.value.filter(item => item.role.trim().toUpperCase() === "ADMIN").length;
});
const editCount = computed(() => {
    return displayItems.value.filter(item => item.role.trim().toUpperCase() === "EDIT").length;
});
const viewCount = computed(() => {
    return displayItems.value.filter(item => item.role.trim().toUpperCase() === "VIEW").length;
});
//Setup rules:
const phoneRule = [
  v => !!v || 'Field is required',
  value => {    
    const pattern = /^\d{3}-\d{3}-\d{4}$/;
    return (pattern.test(value) || value===null )|| 'Invalid Phone Number Format - XXX-XXX-XXXX';
  }
];
const emailRule = [
    v => !!v || 'Field is required',
    value => {
        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return pattern.test(value) || 'Invalid Email Format'
    }
];
//Open Add or Edit Account Dialog
const addOrEditForm = ref(null);
const accountItem = ref({});
const isAdd = ref(-1);
const addOrEditDialog = ref(false);
const addOrEditLoading = ref(false);
async function addOrEditAccount(item){
    if(item)
    {
        isAdd.value = 0;
        accountItem.value = Object.assign({}, item.raw);
    }
    else
    {
        isAdd.value = 1
    }
    addOrEditDialog.value = true;
}

const securityQuestions = ref([
  "What is your mother's maiden name?",
  "What was the name of your first pet?",
  "In what city were you born?",
  "What is your favorite book?",
  "What is the name of your favorite teacher?",
  "What is your favorite color?",
  "What is the make and model of your first car?",
  "What is the name of your childhood best friend?",
  "What is your favorite movie?",
  "What was the street you grew up on?",
  "What is your favorite food?",
  "What is your favorite vacation destination?",
  "What is your favorite sports team?",
  "What is your favorite hobby?",
  "What is your favorite musical artist or band?",
  "What is your favorite historical figure?"
]);


//Reset Password
const resetPw = ref(false);
const repeatPassword = ref();
const passwordsDoNotMatch = computed(() => accountItem.value.password !== repeatPassword.value)
function getCurrentDateTimeString() {
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const now = new Date();

  const dayOfWeek = days[now.getUTCDay()];
  const dayOfMonth = now.getUTCDate().toString().padStart(2, '0');
  const month = months[now.getUTCMonth()];
  const year = now.getUTCFullYear();
  const hours = now.getUTCHours().toString().padStart(2, '0');
  const minutes = now.getUTCMinutes().toString().padStart(2, '0');
  const seconds = now.getUTCSeconds().toString().padStart(2, '0');

  return `${dayOfWeek}, ${dayOfMonth} ${month} ${year} ${hours}:${minutes}:${seconds} GMT`;
}
//Submit Add or Edit Account to Backend
async function submitAddOrEdit()
{
    const {valid} = await addOrEditForm.value.validate();
    const customHeaders = {username: currentUserName, role: currentRole};
    if(resetPw.value && !passwordsDoNotMatch.value){
        piniaStore.setSnackBar("Password Don't Match");
    }
    if(valid ){
        try{
        addOrEditLoading.value = true;
        const usernameDuplicated = displayItems.value.some((obj) => obj.username === accountItem.value.username && obj.account_id !== accountItem.value.account_id);
        if(usernameDuplicated){
            piniaStore.setSnackBar("Username has been used, please use a different one!");
        }
        else{
            if(isAdd.value === 1){        
            //Send Added Account Info To Backend
            const res =  await StoreApi.addAccount(accountItem.value, customHeaders );
            if(res.status === 200)
            {
                accountItem.value.added_by = currentUserName;
                accountItem.value.date_added = getCurrentDateTimeString();
                piniaStore.setSnackBar("Account added successfully", true);
                accountItem.value.account_id = res.data.account_id;
                delete accountItem.value.password;
                displayItems.value.push(accountItem.value);
            }            
            }
            else{
                //Send Editted Account Info to Backend
                accountItem.value.modified_by = currentUserName;
                if(resetPw.value === false){
                    delete accountItem.value.password;
                }
                const res =  await StoreApi.editAccount(accountItem.value, customHeaders);
                if(res.status === 200) {
                    accountItem.value.date_modified = getCurrentDateTimeString();
                    delete accountItem.value.password;
                    const index = displayItems.value.findIndex(obj => obj.account_id === accountItem.value.account_id);
                    if (index !== -1) {
                        displayItems.value[index] = accountItem.value;
                    }
                    piniaStore.setSnackBar("Account modified successfully", true);
                }
            }        
            closeAddOrEdit();
        }            
    }
    catch(error){
        if(error.response.status === 415) {
            piniaStore.setSnackBar(error.response.data.message + ". Please Use A Different Username - Email");
        }
        else if(error.message){
            piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
        }        
            else piniaStore.setSnackBar("Error In Add or Edit Account. Please Contact IT For Support");
    }   
    finally{
        addOrEditLoading.value = false;
    }
    }
    else{
        piniaStore.setSnackBar("Invalid field(s). Please check your input again !");
    }     
}

//Cancel Adding or Editting Account
function closeAddOrEdit(){
    isAdd.value = -1;
    accountItem.value = {};
    repeatPassword.value = '';
    passwordsDoNotMatch.value = false;
    addOrEditDialog.value = false;
    resetPw.value = false;
    addOrEditForm.value.reset();
    addOrEditForm.value.resetValidation();
}

//Delete Account
const delAccount = ref({});
const delLoading = ref(false);
const delDialog = ref(false);
async function deleteAccount(item){
    if(item){
        delDialog.value = true;
        delAccount.value = Object.assign({}, item.raw);
    }    
    else{
        piniaStore.setSnackBar("An error occurs, please contact IT for support!");
    }
}
async function submitDel(){
    try{
        delLoading.value = true;
        //Send data to backend
        const customHeaders = {username: currentUserName, role: currentRole};
        const res = await StoreApi.delAccount(delAccount.value.account_id, customHeaders);
        if(res.status === 200){
            const index = displayItems.value.findIndex(i => i.account_id === delAccount.value.account_id);
            displayItems.value.splice(index, 1);
            piniaStore.setSnackBar("Account deleted successfully", true);
        }
        delLoading.value = false;
        delDialog.value = false;
    }
    catch(error){
        if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
            else piniaStore.setSnackBar("Error In Deleting Account. Please Contact IT For Support");
    }   
}

//Export To CSV file
const exportItem = ref([]);
function exportCSV(){
    exportItem.value = displayItems.value;
    const csvString = [
        [
            'Username',
            'First Name',
            'Last Name',            
            'Phone',
            'Role',
            'Added By',
            'Date Added',
            'Modified By',
            'Modified Date'
        ],
        ...exportItem.value.map( item => [
            item.username,
            item.fname,
            item.lname,           
            item.phone,
            item.role,
            item.added_by,
            item.date_added ? item.date_added.replace(/,/g, '') : '',
            item.modified_by,
            item.date_modified ? item.date_modified.replace(/,/g, '') : ''
        ])
    ]
    .map(e => e.join(","))
    .join("\n");
    const download = document.createElement('a');
    const dateTimeNow = new Date().toISOString().slice(0,-1);
    download.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvString);
    download.target = '_blank';
    download.download = 'Account_' + dateTimeNow + '.csv';
    download.click();
}
</script>
