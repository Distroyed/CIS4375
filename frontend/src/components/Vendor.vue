<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
        <v-row class="justify-center align-center text-center">
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Order By Phone</v-card-title>
                <span class="text-orange-darken-1 text-h4 font-weight-light">{{ onlineCount }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Order By Email</v-card-title>
                <span class="text-red-darken-1 text-h4 font-weight-light">{{emailCount}}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Order By Text</v-card-title>
                <span class="text-purple-darken-1 text-h4 font-weight-light">{{ textCount }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Order By Other</v-card-title>
                <span class="text-green-darken-1 text-h4 font-weight-light">{{ otherCount }}</span>
            </v-card>
        </v-col>
    </v-row>
    <v-card class="mt-10">
    <v-data-table
        :items-per-page="itemsPerPage"
        item-value="vendor_id"
        :headers="headers"
        :loading="loading"
        :search="search"
        :items="displayItems"
        density="compact"
        fixed-header
        class="elevation-6">
        <!-- Toolbar group -->
        <template v-slot:top>
                <v-toolbar flat color="white">
                    <v-toolbar-title >Vendor Management</v-toolbar-title> 
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
                            @click="addOrEditVendor()"
                            >
                                Add Vendor
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
                @click="addOrEditVendor(item)"
                :disabled="loading">
            </v-icon>
            <v-icon
                class="me-2"
                color="red"
                icon="mdi-trash-can"
                size="small"
                @click="deleteVendor(item)"
                :disabled="loading">
            </v-icon>  
        </template>          
            </v-data-table>
            <!-- Add or Edit Vendor Dialog -->
        <v-dialog v-model="addOrEditDialog" persistent width="60%">
            <v-card>
                <v-row class="mt-4 justify-center align-center">
                        <v-card-title v-if="isAdd === 1">
                            Add New Vendor</v-card-title>
                        <v-card-title v-if="isAdd === 0">
                            Edit Current Vendor</v-card-title></v-row>                    
                    <v-card-text>
                        <v-form ref="addOrEditForm">
                            <v-row class="mx-6 justify-center align-center">
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="vendorItem.vendor_name"
                                    label="Vendor Name"
                                    color="primary"
                                    :rules="[ v => !!v || 'Vendor Name is required']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="vendorItem.contact_name"
                                    label="Contact Name"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-textarea
                                    v-model="vendorItem.notes"
                                    label="Notes"
                                    color="primary"
                                    variant="underlined"
                                    clearable
                                    rows="2"
                                    density="compact"
                                    :counter= "' 250'"
                                    ></v-textarea>
                                </v-col>
                            </v-row>          
                            <v-row class="mx-6 justify-center align-center">
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.address"
                                    label="Address"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.city"
                                    label="City"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="3">
                                    <v-autocomplete
                                    v-model="vendorItem.state_id"
                                    label="State"
                                    color="primary"
                                    :rules="[ v => !!v || 'Password is required']"
                                    variant="underlined"
                                    density="compact"
                                    :items="stateList"
                                    item-title="state_abbr"
                                    item-value="state_id"
                                    ></v-autocomplete>
                                </v-col>
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.ZIP"
                                    label="Zip"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                            </v-row>                    
                            <v-row class="mx-6">
                                <v-col cols="4">
                                    <v-autocomplete
                                    v-model="vendorItem.ordering_channel"
                                    label="Ordering Chanel"
                                    color="primary"
                                    clearable
                                    :items="['Via Text','Via Email','Via Phone','Online','Other']"
                                    :rules="[ v => !!v || 'Order Channel is required']"
                                    variant="underlined"></v-autocomplete>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field                                    
                                    v-model="vendorItem.email"
                                    label="Email"
                                    color="primary"
                                    :rules="emailRule"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field                                    
                                    v-model="vendorItem.phone"
                                    label="Phone"
                                    color="primary"
                                    :rules="phoneRule"
                                    variant="underlined"></v-text-field>
                                </v-col>                                
                            </v-row>       
                        </v-form>
                            <v-row justify="center" class="mt-8">
                                <v-card-actions>
                                    <v-btn
                                    variant="flat"
                                    color="green"
                                    width="150"
                                    @click.prevent="submitAddOrEdit()"
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
        <!-- Delete Vendor Dialog -->
        <v-dialog v-model="delDialog" persistent width="60%">
            <v-card>
                <v-row class="mt-4 justify-center align-center">
                    <v-card-title>
                        Delete Vendor Confirmation</v-card-title>
                </v-row>                    
                <v-card-text>
                    <v-row><h4>Are you sure you want to delete this vendor?</h4></v-row>
                    <v-row class="mx-10">
                        <ul>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Vendor Name:</span> {{ delVendor.vendor_name }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Address:</span> {{ delVendor.address}},{{ delVendor.city }},{{ delVendor.state_abbr }},{{ delVendor.zip }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Contact Name:</span> {{ delVendor.contact_name }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Email:</span> {{ delVendor.email }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Phone:</span> {{ delVendor.contact_phone }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Ordering Chanel:</span> {{ delVendor.ordering_channel }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Notes:</span> {{ delVendor.notes }} </p></li>
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
import { ref, computed, watch, onBeforeMount} from 'vue';
import StoreApi from '@/services/StoreApi';
const search = ref(null);
const loading = ref(false)
const itemsPerPage = ref(25);
const piniaStore = useAppStore();
const headers = ref([
    { title: 'Action', align: 'center', key: 'Action'},
    { title: 'Vendor Name', align: 'left', key: 'vendor_name'  },
    { title: 'Address', align: 'left', key: 'address'  },
    { title: 'City', align: 'left', key: 'city'  },
    { title: 'State', align: 'left', key: 'state_abbr'},
    { title: 'Zip Code', align: 'left', key: 'zip' },
    { title: 'Contact Name', align: 'left', key: 'contact_name' },    
    { title: 'Phone Number', align: 'left', key: 'contact_phone' }, 
    { title: 'Email', align: 'left', key: 'email' }, 
    { title: 'Order Channel', align: 'left', key: 'ordering_channel' }, 
    { title: 'Note', align: 'left', key: 'notes' }, 
]);
const displayItems = ref([]);
const stateList = ref([]);
//Fetch Data to Vendor
onBeforeMount(async () => {
    try{
        const res = await StoreApi.getVendor();
        if(res.status === 200){
            displayItems.value = [...res.data];
            console.log(displayItems.value);
        }
        const resState = await StoreApi.getState();
        if(resState.status === 200){
            stateList.value = [...resState.data];
            console.log(stateList.value);
        }
    }
    catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ".Please contact IT for support");
        }
        else piniaStore.setSnackBar("Error in getting Vendor Data. Please contact IT for support");
    }
});

const onlineCount = computed(() => {
  return displayItems.value.filter(item => item.ordering_channel?.trim().toUpperCase() === "ONLINE").length;
});

const textCount = computed(() => {
  return displayItems.value.filter(item => item.ordering_channel?.trim().toUpperCase() === "VIA TEXT").length;
});

const emailCount = computed(() => {
  return displayItems.value.filter(item => (item.ordering_channel?.trim().toUpperCase() === "VIA EMAIL" || item.ordering_channel?.trim().toUpperCase() === "VIA E-MAIL")).length;
});

const otherCount = computed(() => {
    return displayItems.value.length - onlineCount.value - textCount.value - emailCount.value;
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
const vendorItem = ref({});
const isAdd = ref(-1);
const addOrEditDialog = ref(false);
const addOrEditLoading = ref(false);
async function addOrEditVendor(item){
    if(item)
    {
        //This is edit
        isAdd.value = 0;
        vendorItem.value = Object.assign({}, item.raw);
    }
    else
    {
        //This is add
        isAdd.value = 1
    }
    addOrEditDialog.value = true;
}

//Submit Add or Edit Account to Backend
async function submitAddOrEdit()
{
    const {valid} = await addOrEditForm.value.validate();
    if(valid){
        try{
        addOrEditLoading.value = true;
        if(isAdd.value === 1){
            //Send Added Vendor Info To Backend
            vendorItem.value.added_by = piniaStore.currentUserName;
            console.log(vendorItem.value);
            const res =  await StoreApi.addVendor(vendorItem.value);
            if(res.status === 200)
            {
                piniaStore.setSnackBar("Account added successfully");
                displayItems.value.push(vendorItem.value);
            }
        }
        else{
            //Send Editted Vendor Info to Backend
            vendorItem.value.modified_by = piniaStore.currentUserName;
            const res =  await StoreApi.editAccount(vendorItem.value);
            if(res.status === 200) {
                const index = displayItems.value.findIndex(obj => obj.vendor_id === vendorItem.value.vendor_id);
                if (index !== -1) {
                    displayItems.value[index] = vendorItem.value;
                }
            }
        }
        addOrEditLoading.value = false;
        closeAddOrEdit();
    }
    catch(error){
        if(error.response) piniaStore.setSnackBar(error.message + ". Please Contact IT For Support");
            else piniaStore.setSnackBar("Error In Add or Edit Account. Please Contact IT For Support");
    }   
    }
    else{
        piniaStore.setSnackBar("Invalid field(s). Please check your input again !");
    }
}
//Cancel Adding or Editting Vendor
function closeAddOrEdit(){
    isAdd.value = -1;
    vendorItem.value = {};
    addOrEditDialog.value = false;
    addOrEditForm.value.reset();
    addOrEditForm.value.resetValidation();
}

//Delete Account
const delVendor = ref({});
const delLoading = ref(false);
const delDialog = ref(false);
async function deleteVendor(item){
    if(item){
        delDialog.value = true;
        delVendor.value = Object.assign({}, item.raw);
        console.log(delVendor.value);
    }    
    else{
        piniaStore.setSnackBar("An error occurs, please contact IT for support!");
    }
}
async function submitDel(){
    try{
        delLoading.value = true;
        //Send data to backend
        const res = await StoreApi.delVendor(delVendor.value.vendor_id);
        if(res.status === 200){
            const index = displayItems.value.findIndex(i => i.vendor_id === delVendor.value.vendorItem);
            displayItems.value.splice(index, 1);
            piniaStore.setSnackBar("Vendor deleted successfully");
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
            'Vendor Name',
            'Address',
            'City',
            'State',
            'Zip Code',
            'Contact Name',
            'Phone Number',
            'Email',
            'Order Channel',
            'Note'
        ],
        ...exportItem.value.map( item => [
            item.vendor_name,
            item.address,
            item.city,
            item.state_abbr,
            item.zip,
            item.contact_name,
            item.contact_phone,
            item.email,
            item.ordering_channel,
            item.notes
        ])
    ]
    .map(e => e.join(","))
    .join("\n");
    const download = document.createElement('a');
    const dateTimeNow = new Date().toISOString().slice(0,-1);
    download.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvString);
    download.target = '_blank';
    download.download = 'Account_on_' + dateTimeNow + '.csv';
    download.click();
}
</script>