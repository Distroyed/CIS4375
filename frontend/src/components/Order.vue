<template>
<v-container class="mt-10 pa-10" fluid fill-height>
    <v-row justify="center">
    <v-responsive class="d-flex fill-height ma-5">
        <v-alert
        color="info"
        icon="$info"
        title="Order Procedure"
        text="Enter the amount of each items"
        closable 
        ></v-alert>
    <v-card elevation="4" variant="outlined">
        <v-card-title primary-title class="text-center my-4"><h1>Order Supply</h1></v-card-title>
        <v-form ref="orderForm">
            <v-card-text>   
                <v-expansion-panels multiple variant="accordion">
                    <v-expansion-panel>
                        <v-expansion-panel-title expand-icon="mdi-plus" collapse-icon="mdi-minus">
                        <h2 style="text-align: center;">Sushi</h2>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row v-for="sushi in updatedSushiItems" :key="sushi.ID">
                            <v-col cols="3">
                                <v-list lines="two">
                                    <v-list-item
                                ><v-list-item-title>
                                    <p style="font-weight: bold;">{{ sushi.item_name }}</p>
                                </v-list-item-title>
                                <v-list-item-subtitle>$ {{ sushi.PRICE }}</v-list-item-subtitle>
                                </v-list-item>
                                </v-list>              
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="sushi.AMOUNT"
                                label="Amount"
                                :rules="[]"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="sushi.REORDER_POINT"
                                label="Reorder Amount"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-autocomplete
                                v-model="sushi.VENDOR"
                                :items="vendors"
                                item-title="vendor_name"
                                item-value="vendor_id"
                                clearable
                                class="mt-2"
                                variant="outlined"
                                ></v-autocomplete>
                            </v-col>
                        </v-row>    
                        </v-expansion-panel-text>
                    </v-expansion-panel>   
                    <v-expansion-panel>
                        <v-expansion-panel-title expand-icon="mdi-plus" collapse-icon="mdi-minus">
                        <h2 style="text-align: center;">Produce</h2>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row v-for="produce in updatedProduceItems" :key="produce.ID">
                            <v-col cols="3">
                                <v-list lines="two">
                                    <v-list-item
                                ><v-list-item-title>
                                    <p style="font-weight: bold;">{{ produce.item_name }}</p>
                                </v-list-item-title>
                                <v-list-item-subtitle>$ {{ produce.PRICE }}</v-list-item-subtitle>
                                </v-list-item>
                                </v-list>              
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="produce.AMOUNT"
                                label="Amount"
                                :rules="[]"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="produce.REORDER_POINT"
                                label="Reorder Amount"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-autocomplete
                                v-model="produce.VENDOR"
                                :items="vendors"
                                item-title="vendor_name"
                                item-value="vendor_id"
                                clearable
                                class="mt-2"
                                variant="outlined"
                                ></v-autocomplete>
                            </v-col>
                        </v-row>    
                        </v-expansion-panel-text>
                    </v-expansion-panel>   
                    <v-expansion-panel>
                        <v-expansion-panel-title expand-icon="mdi-plus" collapse-icon="mdi-minus">
                        <h2 style="text-align: center;">Other</h2>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row v-for="other in updatedOtherItems" :key="other.ID">
                            <v-col cols="3">
                                <v-list lines="two">
                                <v-list-item
                                ><v-list-item-title>
                                    <p style="font-weight: bold;">{{ other.item_name }}</p>
                                </v-list-item-title>
                                <v-list-item-subtitle>$ {{ other.PRICE }}</v-list-item-subtitle>
                                </v-list-item>
                                </v-list>              
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="other.AMOUNT"
                                label="Amount"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                v-model="other.REORDER_POINT"
                                label="Reorder Amount"
                                class="mt-2"
                                variant="outlined"></v-text-field>                  
                            </v-col>
                            <v-col cols="3">
                                <v-autocomplete
                                v-model="other.VENDOR"
                                :items="vendors"
                                item-title="vendor_name"
                                item-value="vendor_id"
                                clearable
                                class="mt-2"
                                variant="outlined"
                                ></v-autocomplete>
                            </v-col>
                        </v-row>    
                        </v-expansion-panel-text>
                    </v-expansion-panel>                 
            </v-expansion-panels> 
            <v-row justify="center" class="my-5">
                <v-card-actions>
                    <v-btn
                    variant="flat"
                    color="indigo"
                    width="200"
                    class="mx-4"
                    @click="saveData"
                    prepend-icon="mdi-content-save-outline">
                    Submit
                    </v-btn>
                    <v-btn
                    variant="flat"
                    color="red"
                    width="200"
                    class="mx-4"
                    @click="undo"
                    prepend-icon="mdi-cancel">
                    Undo
                    </v-btn>
                </v-card-actions>
                
            </v-row>
            </v-card-text>
        </v-form>
    </v-card>
    </v-responsive>
</v-row>
</v-container>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import StoreApi from '@/services/StoreApi';
const piniaStore = useAppStore();
const originalSushiItems = ref([
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
const originalProduceItem = ref([
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
const originalOtherItems = ref([
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
const updatedSushiItems = ref([]);
const updatedOtherItems = ref([]);
const updatedProduceItems = ref([]);
onBeforeMount( async() => {
    try{
        updatedSushiItems.value = JSON.parse(JSON.stringify(originalSushiItems.value));
        updatedProduceItems.value = JSON.parse(JSON.stringify(originalProduceItem.value));
        updatedOtherItems.value = JSON.parse(JSON.stringify(originalOtherItems.value));
    }
    catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ". Please contact IT for support!");
        }
        else piniaStore.setSnackBar("Error in loading data, please contact IT for support!");
    }
})

const vendors = ref([
    {vendor_id:1, vendor_name:'Hui Lin Inc', address:'6319 Denison Oaks Drive', city:'Katy', state_name:'TX', ZIP:'77494', contact_name:'Li', phone:'832-558-0326', email:'', ordering_channel:'Text', notes:''},
    {vendor_id:2, vendor_name:'Ocean Wave', address:'6319 Denison Oaks Drive', city:'Katy', state_name:'TX', ZIP:'77494', contact_name:'Li', phone:'832-558-0326', email:'', ordering_channel:'Text', notes:''},
    {vendor_id:3, vendor_name:'Food LLC.', address:'6319 Denison Oaks Drive', city:'Katy', state_name:'TX', ZIP:'77494', contact_name:'Li', phone:'832-558-0326', email:'', ordering_channel:'Text', notes:''}
]);

function undo(){
    updatedSushiItems.value = JSON.parse(JSON.stringify(originalSushiItems.value));
    updatedProduceItems.value = JSON.parse(JSON.stringify(originalProduceItem.value));
    updatedOtherItems.value = JSON.parse(JSON.stringify(originalOtherItems.value));
}
async function saveData(){
    console.log(updatedSushiItems.value);
}
</script>