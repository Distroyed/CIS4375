<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
        <v-card >
    <v-data-table
        :items-per-page="itemsPerPage"
        item-value="vendor_id"
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
                                    label="Address"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-area
                                    v-model="vendorItem.notes"
                                    label="Notes"
                                    color="primary"
                                    variant="underlined"
                                    clearable
                                    rows="2"
                                    counter
                                    ></v-text-area>
                                </v-col>
                            </v-row>          
                            <v-row class="mx-6 justify-center align-center">
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.address"
                                    label="Vendor Name"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.city"
                                    label="Address"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.state_name"
                                    label="Last Name"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="3">
                                    <v-text-field
                                    v-model="vendorItem.ZIP"
                                    label="Last Name"
                                    color="primary"
                                    variant="underlined"></v-text-field>
                                </v-col>
                            </v-row>                    
                            <v-row class="mx-6">
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
                                <v-col cols="4">
                                    <v-autocomplete
                                    v-model="vendorItem.ordering_channel"
                                    label="Ordering Chanel"
                                    color="primary"
                                    clearable
                                    :items="['Text','Email','']"
                                    variant="underlined"></v-autocomplete>
                                </v-col>
                            </v-row>       
                        </v-form>
                            <v-row justify="center">
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
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Address:</span> {{ delVendor.address}},{{ delVendor.city }},{{ delVendor.state_name }},{{ delVendor.ZIP }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Contact Name:</span> {{ delVendor.contact_name }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Email:</span> {{ delVendor.email }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Phone:</span> {{ delVendor.phone }} </p></li>
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
    { title: 'State', align: 'left', key: 'state_name'},
    { title: 'Zip Code', align: 'left', key: 'ZIP' },
    { title: 'Contact Name', align: 'left', key: 'contact_name' },    
    { title: 'Phone Number', align: 'left', key: 'phone' }, 
    { title: 'Email', align: 'left', key: 'email' }, 
    { title: 'Order Channel', align: 'left', key: 'ordering_channel' }, 
    { title: 'Note', align: 'left', key: 'notes' }, 
]);
const displayItems = ref([
    {vendor_id:1, vendor_name:'Hui Lin Inc', address:'6319 Denison Oaks Drive', city:'Katy', state_name:'TX', ZIP:'77494', contact_name:'Li', phone:'832-558-0326', email:'', ordering_channel:'Text', notes:''},
]);

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
            //
            displayItems.value.push(vendorItem.value);
        }
        else{
            //Send Editted Vendor Info to Backend
            //
            const index = displayItems.value.findIndex(obj => obj.vendor_id === vendorItem.value.vendor_id);
            if (index !== -1) {
                displayItems.value[index] = vendorItem.value;
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
    }    
    else{
        piniaStore.setSnackBar("An error occurs, please contact IT for support!");
    }
}
async function submitDel(){
    try{
        delLoading.value = true;
        //Send data to backend
        //
            const index = displayItems.value.findIndex(i => i.vendor_id === delVendor.value.vendorItem);
            displayItems.value.splice(index, 1)
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
            'Email',
            'Phone',
            'Role',
            'Added By',
            'Date Added'
        ],
        ...exportItem.value.map( item => [
            item.username,
            item.fname,
            item.lname,
            item.email,
            item.phone,
            item.role,
            item.added_by,
            item.Enabled,
            item.date_added
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