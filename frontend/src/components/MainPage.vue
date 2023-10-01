<template>
    <v-card class="my-5">
    <v-data-table
        :items-per-page="itemsPerPage"
        item-value="ID"
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
                    <v-toolbar-title >Food Inventory Report</v-toolbar-title> 
                    <v-divider
                            inset
                            vertical
                            class="mx-5"
                    ></v-divider>   
                    <v-spacer></v-spacer>
                    <v-spacer></v-spacer>
                    <v-btn
                            variant="flat"
                            color="green"
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
        </template>          
            </v-data-table>
        </v-card>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch } from 'vue';
import StoreApi from '@/services/StoreApi';
const search = ref(null);
const loading = ref(false)
const itemsPerPage = ref(25);
const piniaStore = useAppStore();
//Show Exceptional Account
const headers = ref([
    { title: 'Action', align: 'center', key: 'Action', width: 20},
    { title: 'Ingredient', align: 'center', key: 'INGREDIENT_NAME', width: 40  },
    { title: 'Units', align: 'center', key: 'UNIT', width: 10  },
    { title: 'Amount', align: 'center', key: 'AMOUNT', width: 40  },
    { title: 'Reorder Amount', align: 'center', key: 'REORDER_POINT', width: 40},
    { title: 'Vendor', align: 'center', key: 'VENDOR', width: 40 },
    { title: 'Price', align: 'center', key: 'PRICE', width: 40 },    
]);

const displayItems = ref([
    {ID:1, INGREDIENT_NAME:'Rice', UNIT:'Pack', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:2, INGREDIENT_NAME:'Nori', UNIT:'Pack', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:3, INGREDIENT_NAME:'Mirin', UNIT:'Box', AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:4, INGREDIENT_NAME:'Carrot', UNIT:'Bag', AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:5, INGREDIENT_NAME:'Avocado', UNIT:'Box', AMOUNT:'2', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:6, INGREDIENT_NAME:'Salmon', UNIT:'Box', AMOUNT:'30', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:7, INGREDIENT_NAME:'Wasabi', UNIT:'Box', AMOUNT:'21', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:8, INGREDIENT_NAME:'Soy Sauce', UNIT:'Box', AMOUNT:'10', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:9, INGREDIENT_NAME:'Salt', UNIT:'Box', AMOUNT:'15', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
    {ID:10, INGREDIENT_NAME:'Sugar', UNIT:'Box', AMOUNT:'20', REORDER_POINT:'10', VENDOR:'Food LLC.', PRICE:'1000.00'},
]);
</script>