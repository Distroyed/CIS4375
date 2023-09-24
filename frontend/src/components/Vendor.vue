<template>
    <v-container class="mt-10 pa-10" fluid fill-height>
        <v-card >
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
</script>