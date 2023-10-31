<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
    <v-row class="justify-center align-center text-center">
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Sushi</v-card-title>
                <span class="text-orange-darken-1 text-h4 font-weight-light">{{ sushiItems.length }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Produce</v-card-title>
                <span class="text-red-darken-1 text-h4 font-weight-light">{{ produceItem.length }}</span>
            </v-card>
        </v-col>
        <v-col cols="2">
            <v-card elevation="1" class="pb-3">
                <v-card-title class="text-overline">Other</v-card-title>
                <span class="text-purple-darken-1 text-h4 font-weight-light">{{ otherItems.length }}</span>
            </v-card>
        </v-col>
    </v-row>
    <v-row justify="center" class="mt-10">
        <v-col cols="4">
        <v-autocomplete
        v-model="selectSupplyType"
        label="Select Supply Type"
        color="primary"
        density="compact"
        variant="underlined"
        item-title="item_type_desc"
        item-value="item_type_id"
        :items="itemType"
        prepend-icon="mdi-format-list-bulleted-type"
        clearable></v-autocomplete>
    </v-col>
    </v-row>
    <Transition name="fade" mode="out-in">
    <v-card v-if="selectSupplyType">
    <v-data-table
        :items-per-page="itemsPerPage"
        item-value="supply_id"
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
                    <v-toolbar-title >{{selectSupplyType}} Supply Management</v-toolbar-title> 
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
                            class="mr-5"
                            @click="addOrEditSupply()"
                            >
                                Add More
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
                color="blue"
                icon="mdi-magnify"
                size="small"
                @click="viewPriceHist(item)"
                :disabled="loading">
            </v-icon>
            <v-icon
                class="me-2"
                color="green"
                icon="mdi-pencil"
                size="small"
                @click="addOrEditSupply(item)"
                :disabled="loading">
            </v-icon>   
            <v-icon
                class="me-2"
                color="red"
                icon="mdi-trash-can"
                size="small"
                @click="deleteSupply(item)"
                :disabled="loading">
            </v-icon>  
        </template>          
            </v-data-table>
<!-- Add or Edit Supply Dialog -->
<v-dialog v-model="addOrEditDialog" persistent width="60%">
            <v-card>
                <v-row class="mt-4 justify-center align-center">
                        <v-card-title v-if="isAdd === 1">
                            Add New Supply</v-card-title>
                        <v-card-title v-if="isAdd === 0">
                            Edit Current Supply</v-card-title></v-row>                    
                    <v-card-text>
                        <v-form ref="addOrEditForm">
                            <v-row class="mx-6 justify-center align-center">
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="supplyItem.item_name"
                                    label="Supply Name"
                                    color="primary"
                                    :rules="[ v => !!v || 'Vendor Name is required']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-text-field
                                    v-model="supplyItem.reorder_point"
                                    label="Reorder Point"
                                    color="primary"
                                    type="number"
                                    :rules="[ v => !!v || 'Reorder Point is required']"
                                    variant="underlined"></v-text-field>
                                </v-col>
                                <v-col cols="4">
                                    <v-textarea
                                    v-model="supplyItem.notes"
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
                                <v-col cols="6">
                                    <v-autocomplete
                                    v-model="supplyItem.item_type_id"
                                    label="Select Supply Type"
                                    :items="itemType"
                                    color="primary"
                                    density="compact"
                                    variant="underlined"
                                    prepend-icon="mdi-format-list-bulleted-type"
                                    clearable
                                    item-title="item_type_desc"
                                    item-value="item_type_id"
                                    ></v-autocomplete>
                                </v-col>
                                <v-col cols="6">
                                    <v-autocomplete
                                    v-model="supplyItem.vendor_id"
                                    label="Select Vendor"
                                    :items="vendor"
                                    color="primary"
                                    density="compact"
                                    variant="underlined"
                                    prepend-icon="mdi-format-list-bulleted-type"
                                    clearable
                                    item-title="vendor_name"
                                    item-value="vendor_id"
                                    ></v-autocomplete>
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
        <!-- Delete Supply Dialog -->
        <v-dialog v-model="delDialog" persistent width="60%">
            <v-card>
                <v-row class="mt-4 justify-center align-center">
                    <v-card-title>
                        Delete Supply Confirmation</v-card-title>
                </v-row>                    
                <v-card-text>
                    <v-row><h4>Are you sure you want to delete this Supply?</h4></v-row>
                    <v-row class="mx-10">
                        <ul>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Item Name:</span> {{ delSupply.item_name }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Reorder Point:</span> {{ delSupply.reorder_point }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Vendor Name:</span> {{ delSupply.vendor_name }} </p></li>
                                <li><p style="font-size:15px"><span style="font-weight: bold;">Notes:</span> {{ delSupply.notes }} </p></li>
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
    </Transition>
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
const headers = ref([
    { title: 'Action', align: 'center', key: 'Action'},
    { title: 'Item Name', align: 'left', key: 'item_name'  },
    { title: 'Quantity', align: 'left', key: 'quantity'  },
    { title: 'Reorder Amount', align: 'left', key: 'reorder_point '},
    { title: 'Vendor', align: 'left', key: 'vendor_name' },
    { title: 'Note', align: 'left', key: 'notes' },    
]);
const displayItems = computed(() =>{
    if(selectSupplyType.value === 1){
        return sushiItems.value;
    }
    else if(selectSupplyType.value === 2){
        return produceItem.value;
    }
    else{
        return otherItems.value;
    }
});
const sushiItems = ref([]);
const produceItem = ref([]);
const otherItems = ref([]);
const selectSupplyType = ref();
const itemType = ref([]);
const vendor = ref([]);
const allSupply = ref([])
//Fetch Data to table
onBeforeMount(async () => {
    try{
        const res = await StoreApi.getSupply();
        console.log(res.data)
        if(res.status === 200){
            allSupply.value = res.data;
            sushiItems.value = allSupply.value.filter((item) => item.item_type_id === 1);
            produceItem.value = allSupply.value.filter((item) => item.item_type_id === 2);
            otherItems.value = allSupply.value.filter((item) => item.item_type_id === 3);
            itemType.value = (await StoreApi.getItemType()).data;
        }
        
        vendor.value = (await StoreApi.getVendor()).data;
    }
    catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ".Please contact IT for support");
        }
        else piniaStore.setSnackBar("Error in getting Supply Data. Please contact IT for support");
    }
});


//View Price History
const priceHistItem = ref({});
async function viewPriceHist(item){
    console.log(item.raw);
}

//Open Add or Edit Account Dialog
const addOrEditForm = ref(null);
const supplyItem = ref({});
const isAdd = ref(-1);
const addOrEditDialog = ref(false);
const addOrEditLoading = ref(false);
async function addOrEditSupply(item){
    if(item)
    {
        //This is edit
        isAdd.value = 0;
        supplyItem.value = Object.assign({}, item.raw);
    }
    else
    {
        //This is add
        isAdd.value = 1
    }
    addOrEditDialog.value = true;
}

//Submit Add or Edit Supply to Backend
async function submitAddOrEdit()
{
    const {valid} = await addOrEditForm.value.validate();
    if(valid){
        try{
        addOrEditLoading.value = true;
        if(isAdd.value === 1){
            //Send Added Supply Info To Backend
            supplyItem.value.added_by = piniaStore.currentUserName;
            console.log(supplyItem.value);
            const res =  await StoreApi.addSupply(supplyItem.value);
            if(res.status === 200)
            {
                //GET RETURN ID
                piniaStore.setSnackBar("Supply added successfully");
                allSupply.value.push(supplyItem.value);
            }
        }
        else{
            //Send Editted Supply Info to Backend
            supplyItem.value.modified_by = piniaStore.currentUserName;
            const res =  await StoreApi.editSupply(supplyItem.value);
            if(res.status === 200) {
                const index = allSupply.value.findIndex(obj => obj.supply_id === supplyItem.value.supply_id);
                if (index !== -1) {
                    allSupply.value[index] = supplyItem.value;
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
//Cancel Adding or Editting Supply
function closeAddOrEdit(){
    isAdd.value = -1;
    supplyItem.value = {};
    addOrEditDialog.value = false;
    addOrEditForm.value.reset();
    addOrEditForm.value.resetValidation();
}

//Delete Supply
const delSupply = ref({});
const delLoading = ref(false);
const delDialog = ref(false);
async function deleteSupply(item){
    if(item){
        delDialog.value = true;
        delSupply.value = Object.assign({}, item.raw);
        console.log(delSupply.value);
    }    
    else{
        piniaStore.setSnackBar("An error occurs, please contact IT for support!");
    }
}
async function submitDel(){
    try{
        delLoading.value = true;
        //Send data to backend
        const res = await StoreApi.delSupply(delSupply.value.supply_id);
        if(res.status === 200){
            const index = allSupply.value.findIndex(i => i.supply_id === delSupply.value.supply_id);
            allSupply.value.splice(index, 1);
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
            'Item Type',
            'Item Name',
            'Quantity',
            'Reorder Point',
            'Price',
            'Note',
            'Vendor',
            'Added By',
            'Date Added',
            'Modified By',
            'Modified Date'
        ],
        ...exportItem.value.map( item => [
            item.item_type_desc,
            item.item_name,
            item.quantity,
            item.reorder_point,
            item.price,
            item.notes,
            item.vendor_name,
            item.added_by,            
            item.date_added,
            item.modified_by,
            item.date_modified
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