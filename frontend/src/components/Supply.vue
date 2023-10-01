<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
    <v-row justify="center">
        <v-col cols="4">
        <v-autocomplete
        v-model="selectSupplyType"
        label="Select Supply Type"
        color="primary"
        density="compact"
        variant="underlined"
        :items="['Sushi','Produce','Other']"
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
                :disabled="loading">
            </v-icon>   
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
                color="red"
                icon="mdi-trash-can"
                size="small"
                :disabled="loading">
            </v-icon>  
        </template>          
            </v-data-table>
        </v-card>
    </Transition>
    </v-container>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch } from 'vue';
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
    { title: 'Vendor', align: 'left', key: 'VENDOR' },
    { title: 'Note', align: 'left', key: 'Notes' },    
]);
const displayItems = computed(() =>{
    if(selectSupplyType.value == 'Sushi'){
        return sushiItems.value;
    }
    else if(selectSupplyType.value == 'Produce'){
        return produceItem.value;
    }
    else{
        return otherItems.value;
    }
});
const sushiItems = ref([
    {ID:1, item_name:'Escolar', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:2, item_name:'Ika Salad',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Ocean Wave', PRICE:'1000.00'},
    {ID:3, item_name:'Katsu Mirin (banito seasoning)', AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Wismettac', PRICE:'1000.00'},
    {ID:4, item_name:'Masago - habanero', AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Wismettac', PRICE:'1000.00'},
    {ID:5, item_name:'Masago - jalapeno',  AMOUNT:'2', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:6, item_name:'Masago - orange', AMOUNT:'30', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:7, item_name:'Nori - full sheet',  AMOUNT:'21', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:8, item_name:'Poke bowls',  AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:9, item_name:'Salmon',  AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
    {ID:10, item_name:'Soft Shell Crab - hotel',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Kazy.', PRICE:'1000.00'},
]);
const produceItem = ref([
    {ID:1, item_name:'Enoki Mushroom', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:2, item_name:'King Mushroom',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:3, item_name:'Avocados', AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:4, item_name:'Carrot', AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:5, item_name:'Avocado',  AMOUNT:'2', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:6, item_name:'Eggs', AMOUNT:'30', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:7, item_name:'Cilantro',  AMOUNT:'21', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:8, item_name:'Celery',  AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:9, item_name:'Jalapenos',  AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:10, item_name:'Mango',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
]);
const otherItems = ref([
    {ID:1, item_name:'16 oz soup container', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:2, item_name:'2 oz cups w/lids',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:3, item_name:'8 oz soup container', AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:4, item_name:'Coconut Milk', AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:5, item_name:'Honey',  AMOUNT:'2', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:6, item_name:'Maple syrup', AMOUNT:'30', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:7, item_name:'Salt',  AMOUNT:'21', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:8, item_name:'Sugar',  AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:9, item_name:'Halal Chicken - grilled',  AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:10, item_name:'Corn Kernnels',  AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
]);
const selectSupplyType = ref();

//View Price History
const priceHistItem = ref({});
async function viewPriceHist(item){
    console.log(item.raw);
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