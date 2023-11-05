<template>
    <v-card class="mx-auto mt-16" elevation="5"  style="background-color: rgba(255, 255, 255, 0.8);">
        <v-btn prepend-icon="mdi-restore" color="indigo-darken-3" width="150" variant="flat" size="small" class="mx-5 my-5" :loading="loading" @click="goback">
                        Go Back</v-btn>
        <v-card-title>Report History</v-card-title>
        <v-card-text>
            <v-expansion-panels variant="accordion">
                <v-expansion-panel
                v-for="report in reportHist"
                :key="report.report_group"
                >
                    <v-expansion-panel-title expand-icon="mdi-menu-down">
                        {{ report.report_group }}
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-btn prepend-icon="mdi-microsoft-excel" 
                        color="green" 
                        variant="flat" 
                        class="my-2"
                        size="small" :loading="loading" @click="exportCSV(report.data)">
                        Export To CSV</v-btn>
                        <v-data-table
                            :headers="headers"
                            :loading="loading"
                            :items="report.data"
                            :items-per-page="itemsPerPage"
                            density="compact"
                            fixed-header
                            class="elevation-5">
                        </v-data-table>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-card-text>

    </v-card>
</template>
<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
const piniaStore = useAppStore();
const router = useRouter();
import StoreApi from '@/services/StoreApi';
const reportHist = ref([]);
const loading = ref(false);
const headers = ref([
    { title: 'Date', align: 'left', key: 'modified_date'  },
    { title: 'Item', align: 'left', key: 'item_name'  },
    { title: 'Quantity Order', align: 'left', key: 'qty_ordered'  },
    { title: 'Price', align: 'left', key: 'price'},
    { title: 'Vendor', align: 'left', key: 'vendor_name' },
    { title: 'Contact Phone', align: 'left', key: 'contact_phone' },
    { title: 'Order Phone', align: 'left', key: 'order_phone' },
    { title: 'Email', align: 'left', key: 'email' },
    { title: 'Ordering Channel', align: 'left', key: 'ordering_channel' },
]);
const itemsPerPage = ref(25);
onBeforeMount(async () => {
    try{
        loading.value = true;
        const res = await StoreApi.getReportHistory();
        if(res.status === 200){
            reportHist.value = res.data;
            //console.log(reportHist.value);
        }
    }
    catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ".Please contact IT for support");
        }
        else piniaStore.setSnackBar("Error in getting Account Data. Please contact IT for support");
    }
    finally{
        loading.value = false;
    }
});
function goback(){
    router.push({name: 'Order'});
}

//Export To CSV file
const exportItem = ref([]);
function exportCSV(data){
    exportItem.value = data;
    const report_group = data[0].report_group
    const csvString = [
        [
            'Report Date',
            'Item',
            'Quantity Order',            
            'Price',
            'Vendor Name',
            'Contact Name',
            'Contact Phone',
            'Order Phone',
            'Email',
            'Ordering Channel'
        ],
        ...exportItem.value.map( item => [
            item.modified_date.replace(/,/g, ''),
            item.item_name,
            item.qty_ordered,           
            item.price,
            item.vendor_name,
            item.contact_name,
            item.contact_phone,
            item.order_phone,
            item.email,
            item.ordering_channel
        ])
    ]
    .map(e => e.join(","))
    .join("\n");
    const download = document.createElement('a');
    download.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvString);
    download.target = '_blank';
    download.download = 'Report_' + report_group + '.csv';
    download.click();
}
</script>
