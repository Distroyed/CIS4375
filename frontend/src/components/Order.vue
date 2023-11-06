<template>
<v-container class="mt-10 pa-10" fluid fill-height>
    <v-row justify="center">
    <v-responsive class="d-flex fill-height ma-5">
    <div v-if="!generateReport">
        <v-alert
        color="info"
        icon="$info"
        title="Order Procedure"
        text="Enter the current quantity of each items"
        closable 
        ></v-alert>
    <v-card elevation="4" variant="outlined">
        <v-card-title primary-title class="text-center my-3"><h1>Order Supply</h1></v-card-title>
        <v-form ref="orderForm">
            <v-card-text>   
                <v-tabs
                v-model="tab"
                color="deep-purple-accent-4"
                align-tabs="center"
                >
                <v-tab value="one" >SUSHI</v-tab>
                <v-tab value="two" >PRODUCE</v-tab>
                <v-tab value="three">OTHER</v-tab>
                </v-tabs>
                <v-window v-model="tab" class="mt-5">
                    <v-window-item value="one" >
                        <v-row v-for="sushi in updatedSushiItems" :key="sushi.supply_id">
                        <v-col cols="3">
                            <v-list lines="two">
                                <v-list-item
                            ><v-list-item-title>
                                <p style="font-weight: bold;">{{ sushi.item_name }}</p>
                            </v-list-item-title>
                            <v-list-item-subtitle>$ {{ sushi.price }}</v-list-item-subtitle>
                            </v-list-item>
                            </v-list>              
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="sushi.quantity"
                            label="Current Quantity"
                            :rules=rules
                            class="mt-2"
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="sushi.reorder_point"
                            label="Reorder Amount"
                            class="mt-2"
                            :rules=rules
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-autocomplete
                            v-model="sushi.vendor_id"
                            :items="vendors"
                            item-title="vendor_name"
                            item-value="vendor_id"
                            clearable
                            class="mt-2"
                            disabled
                            variant="outlined"
                            ></v-autocomplete>
                        </v-col>
                        </v-row>    
                    </v-window-item>
                    <v-window-item value="two">
                        <v-row v-for="produce in updatedProduceItems" :key="produce.supply_id">
                        <v-col cols="3">
                            <v-list lines="two">
                                <v-list-item
                            ><v-list-item-title>
                                <p style="font-weight: bold;">{{ produce.item_name }}</p>
                            </v-list-item-title>
                            <v-list-item-subtitle>$ {{ produce.price }}</v-list-item-subtitle>
                            </v-list-item>
                            </v-list>              
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="produce.quantity"
                            label="Current Quantity"
                            :rules=rules
                            class="mt-2"
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="produce.reorder_point"
                            label="Reorder Amount"
                            :rules=rules
                            class="mt-2"
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-autocomplete
                            v-model="produce.vendor_id"
                            :items="vendors"
                            item-title="vendor_name"
                            item-value="vendor_id"
                            clearable
                            class="mt-2"
                            variant="outlined"
                            disabled
                            ></v-autocomplete>
                        </v-col>
                        </v-row>    
                    </v-window-item>
                    <v-window-item value="three">
                        <v-row v-for="other in updatedOtherItems" :key="other.supply_id">
                        <v-col cols="3">
                            <v-list lines="two">
                            <v-list-item
                            ><v-list-item-title>
                                <p style="font-weight: bold;">{{ other.item_name }}</p>
                            </v-list-item-title>
                            <v-list-item-subtitle>$ {{ other.price }}</v-list-item-subtitle>
                            </v-list-item>
                            </v-list>              
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="other.quantity"
                            label="Current Quantity"
                            :rules=rules
                            class="mt-2"
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-text-field
                            v-model="other.reorder_point"
                            label="Reorder Amount"
                            :rules=rules
                            class="mt-2"
                            variant="outlined"></v-text-field>                  
                        </v-col>
                        <v-col cols="3">
                            <v-autocomplete
                            v-model="other.vendor_id"
                            :items="vendors"
                            item-title="vendor_name"
                            item-value="vendor_id"
                            clearable
                            class="mt-2"
                            variant="outlined"
                            disabled
                            ></v-autocomplete>
                        </v-col>
                        </v-row>    
                    </v-window-item>
                </v-window>                
            <v-row justify="center" class="my-5">
                <v-card-actions>
                    <v-btn
                    variant="flat"
                    width="250"
                    color="purple"
                    class="mx-4"
                    @click.prevent="goToReportHistory" 
                    :loading="loading"
                    prepend-icon="mdi-clipboard-text-clock-outline"
                    >
                    View Report History</v-btn>
                    <v-btn
                    variant="flat"
                    color="indigo"
                    width="250"
                    class="mx-4"
                    @click="saveData"
                    :disabled="currentRole == 'view'"
                    :loading="loading"
                    prepend-icon="mdi-content-save-outline">
                    Generate Report
                    </v-btn>
                    <v-btn
                    variant="flat"
                    color="red"
                    width="250"
                    class="mx-4"
                    @click="undo"
                    :disabled="currentRole == 'view' || loading==true"
                    prepend-icon="mdi-cancel">
                    Undo Report
                    </v-btn>
                </v-card-actions>
            </v-row>
            </v-card-text>
        </v-form>
    </v-card>
    </div>

    <div v-if="generateReport">
        <v-card elevation="4" variant="outlined">
        <v-card-title primary-title class="text-center my-3"><h1>Order Report</h1></v-card-title>
        <v-form ref="orderForm">
            <v-card-text>   
                <v-tabs
                v-model="tab"
                color="deep-purple-accent-4"
                align-tabs="center"
                >
                <v-tab value="one" >SUSHI</v-tab>
                <v-tab value="two" >PRODUCE</v-tab>
                <v-tab value="three">OTHER</v-tab>
                </v-tabs>
                <v-window v-model="tab" class="mt-5">
                    <v-window-item value="one" >
                                <v-table>                                
                                <thead>
                                <tr>
                                    <th class="text-left">
                                    Item Name
                                    </th>
                                    <th class="text-left">
                                    Current Price
                                    </th>
                                    <th class="text-left">
                                    Quantity Order
                                    </th>
                                    <th class="text-left">
                                    Total Cost
                                    </th>
                                    <th class="text-left">
                                    Vendor Name
                                    </th>
                                    <th class="text-left">
                                    Ordering Channel
                                    </th>
                                    <th class="text-left">
                                    Contact Phone
                                    </th>
                                    <th class="text-left">
                                    Order Phone
                                    </th>
                                    <th class="text-left">
                                    Email
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr
                                    v-for="item in reportSushi"
                                    :key="item.supply_id"
                                >
                                    <td>{{ item.item_name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.qty_ordered }}</span></td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.total_cost }}</span></td>
                                    <td>{{ item.vendor_name }}</td>
                                    <td>{{ item.ordering_channel }}</td>
                                    <td>{{ item.contact_phone }}</td>
                                    <td>{{ item.order_phone }}</td>
                                    <td>{{ item.email }}</td>
                                </tr>
                                </tbody>
                            </v-table>
                        </v-window-item>
                            <v-window-item value="two" >
                                <v-table>                                
                                <thead>
                                <tr>
                                    <th class="text-left">
                                    Item Name
                                    </th>
                                    <th class="text-left">
                                    Current Price
                                    </th>
                                    <th class="text-left">
                                    Quantity Order
                                    </th>
                                    <th class="text-left">
                                    Total Cost
                                    </th>
                                    <th class="text-left">
                                    Vendor Name
                                    </th>
                                    <th class="text-left">
                                    Ordering Channel
                                    </th>
                                    <th class="text-left">
                                    Contact Phone
                                    </th>
                                    <th class="text-left">
                                    Order Phone
                                    </th>
                                    <th class="text-left">
                                    Email
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr
                                    v-for="item in reportProduce"
                                    :key="item.supply_id"
                                >
                                    <td>{{ item.item_name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.qty_ordered }}</span></td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.total_cost }}</span></td>
                                    <td>{{ item.vendor_name }}</td>
                                    <td>{{ item.ordering_channel }}</td>
                                    <td>{{ item.contact_phone }}</td>
                                    <td>{{ item.order_phone }}</td>
                                    <td>{{ item.email }}</td>
                                </tr>
                                </tbody>
                            </v-table>
                            </v-window-item>
                                <v-window-item value="three" >
                                <v-table>                                
                                <thead>
                                <tr>
                                    <th class="text-left">
                                    Item Name
                                    </th>
                                    <th class="text-left">
                                    Current Price
                                    </th>
                                    <th class="text-left">
                                    Quantity Order
                                    </th>
                                    <th class="text-left">
                                    Total Cost
                                    </th>
                                    <th class="text-left">
                                    Vendor Name
                                    </th>
                                    <th class="text-left">
                                    Ordering Channel
                                    </th>
                                    <th class="text-left">
                                    Contact Phone
                                    </th>
                                    <th class="text-left">
                                    Order Phone
                                    </th>
                                    <th class="text-left">
                                    Email
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr
                                    v-for="item in reportOther"
                                    :key="item.supply_id"
                                >
                                    <td>{{ item.item_name }}</td>
                                    <td>{{ item.price }}</td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.qty_ordered }}</span></td>
                                    <td><span style="color: red; font-weight: bold;">{{ item.total_cost }}</span></td>
                                    <td>{{ item.vendor_name }}</td>
                                    <td>{{ item.ordering_channel }}</td>
                                    <td>{{ item.contact_phone }}</td>
                                    <td>{{ item.order_phone }}</td>
                                    <td>{{ item.email }}</td>
                                </tr>
                                </tbody>
                            </v-table>
                            </v-window-item>    
                </v-window>                
            <v-row justify="center" class="my-5">
                <v-row justify="center" class="mt-8">
                        <v-card-actions>                            
                            <v-btn
                            variant="flat"
                            width="200"
                            color="green"
                            @click.prevent="exportToXLSX()" 
                            prepend-icon="mdi-microsoft-excel"
                            >
                            Export To XLSX</v-btn>
                            <v-btn
                            variant="flat"
                            width="200"
                            color="blue"
                            @click.prevent="exportToCSV()" 
                            prepend-icon="mdi-microsoft-excel"
                            >
                            Export To CSV</v-btn>                            
                            <v-btn
                            variant="flat"
                            width="200"
                            color="red"
                            @click.prevent="Complete()" 
                            prepend-icon="mdi-restore"
                            >
                            Back To Order</v-btn>
                        </v-card-actions>
                    </v-row>
            </v-row>
            </v-card-text>
        </v-form>
    </v-card>
    </div>
    </v-responsive>
</v-row>
<v-dialog v-model="loading" persistent width="25%">
            <v-card class="align-center justify-center text-center my-5 mx-5">
                <v-card-title>Report is generating...</v-card-title>
                <v-progress-circular
                class="my-8"
                :size="150"
                :width="8"
                color="indigo"                
                indeterminate                
                ></v-progress-circular>
            </v-card>
        </v-dialog>
</v-container>
</template>
<script setup>
import { useRouter } from 'vue-router';
import { useAppStore } from '@/store/app'
import { ref, computed, watch, onBeforeMount } from 'vue';
import StoreApi from '@/services/StoreApi';

//retrieve data from session storage
const loginSuccess = sessionStorage.getItem('loginSuccess');
const currentUserName = sessionStorage.getItem('currentUserName');
const currentRole = sessionStorage.getItem('currentRole');

const router = useRouter();
const piniaStore = useAppStore();
const originalSushiItems = ref([])
const originalProduceItem = ref([])
const originalOtherItems = ref([])
const updatedSushiItems = ref([]);
const updatedOtherItems = ref([]);
const updatedProduceItems = ref([]);
const allSupply = ref([]);
const itemType = ref([]);
const vendors = ref([]);
const tab = ref("one");
const rules = ref([
  v => v !== null || 'Field is required',
  v => v >= 0 || 'Field must be greater than or equal to 0'
]);
async function getData(){
    try{
        const res = await StoreApi.getSupply();
        if(res.status === 200){
            allSupply.value = res.data;
            originalSushiItems.value = allSupply.value.filter((item) => item.item_type_id === 1);
            originalProduceItem.value = allSupply.value.filter((item) => item.item_type_id === 2);
            originalOtherItems.value = allSupply.value.filter((item) => item.item_type_id === 3);
            itemType.value = (await StoreApi.getItemType()).data;
        }
        vendors.value = (await StoreApi.getVendor()).data;
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
}
onBeforeMount( async() => {
    getData()
});
function undo(){
    updatedSushiItems.value = JSON.parse(JSON.stringify(originalSushiItems.value));
    updatedProduceItems.value = JSON.parse(JSON.stringify(originalProduceItem.value));
    updatedOtherItems.value = JSON.parse(JSON.stringify(originalOtherItems.value));
}
function generateUniqueID() {
  const timestamp = new Date().getTime().toString(36); // Convert timestamp to base36
  const randomChars = Math.random().toString(36).substr(2, 5); // Generate random characters

  return `${timestamp}${randomChars}`;
}
const orderForm = ref(null);
const generateReport = ref(false);
const reportSushi = ref([]);
const reportProduce = ref([]);
const reportOther = ref([]);
const loading = ref(false);
const groupIDName = ref(null);
async function saveData(){
    const {valid} = await orderForm.value.validate();    
    if(valid){
        loading.value = true;
        reportSushi.value = calculateSupplyValues(updatedSushiItems.value);
        reportProduce.value = calculateSupplyValues(updatedProduceItems.value);
        reportOther.value = calculateSupplyValues(updatedOtherItems.value);
        const finalReport = [...reportSushi.value, ...reportProduce.value, ...reportOther.value];
        const groupID = generateUniqueID();
        groupIDName.value = groupID
        const finalReportWithID = finalReport.map(obj =>({
            ...obj,
            report_group: groupID
        }));
        try{
            const customHeaders = {username: currentUserName, role: currentRole};
            const res = await StoreApi.updateTransaction(finalReportWithID, customHeaders);
            if(res.status === 200){
                piniaStore.setSnackBar("Report Created Successfully", true);
                generateReport.value = true;
                exportToXLSX();
            }            
        }
        catch(error){
        if(error.message){
            piniaStore.setSnackBar(error.message + ". Please contact IT for support!");
        }
        else piniaStore.setSnackBar("Error in generating report, please contact IT for support!");
        }
        finally{
            loading.value = false;
        }
    }
    else{
        piniaStore.setSnackBar("Invalid field(s). Please check your input again !");
    }
}

function calculateSupplyValues(array) {
  return array
    .map((obj) => {
    const qty_ordered = obj.reorder_point - obj.quantity;
    obj.qty_ordered = qty_ordered >= 0 ? qty_ordered : 0;
    
    if (!obj.price || obj.price === "None") {
      obj.price = 0;
    } else {
      obj.price = Number(obj.price).toFixed(2);
    }    
    obj.total_cost = Number(obj.qty_ordered * obj.price).toFixed(2);
    return obj;
    })
}

async function Complete(){
    generateReport.value = false;
    getData();
    tab.value = "one";
}

//Export To CSV file
function exportToCSV(){
    const tabs = [
        {
            tabName: 'Sushi',
            data: reportSushi.value, 
        },
        {
            tabName: 'Produce',
            data: reportProduce.value, 
        },
        {
            tabName: 'Other',
            data: reportOther.value, 
        },
    ];

    const csvString =[];
    tabs.forEach(tab => {
        csvString.push([tab.tabName]);

        // Add headers
        csvString.push([
            'Item Name',
            'Current Price',
            'Quantity Order',
            'Total Cost',
            'Vendor Name',
            'Ordering Channel',
            'Contact Phone',
            'Order Phone',
            'Email'
        ]);

        // Add tab data
        csvString.push(
            ...tab.data.map(item => [
                item.item_name,
                item.price,
                item.qty_ordered,
                item.total_cost,
                item.vendor_name,
                item.ordering_channel,
                item.contact_phone,
                item.order_phone,
                item.email
            ])
        );

        // Separate tabs with an empty line
        csvString.push([]);
    });
    const csvData = csvString
        .map(section => section.join(','))
        .join('\n');
    // Create a Blob from the CSV data
    const blob = new Blob([csvData], { type: 'text/csv' });

    // Create a URL for the Blob
    const blobUrl = URL.createObjectURL(blob);
    // Create a download link for the user to save the file
    const dateTimeNow = new Date().toISOString().slice(0,-1);
    const downloadLink = document.createElement('a');
    downloadLink.href = blobUrl;
    downloadLink.download = 'Report_' + dateTimeNow + '_' + groupIDName.value + '.csv';
    downloadLink.style.display = 'none';
    // Trigger a click event to prompt the user to save the file
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);

    // Ensure the URL is revoked when no longer needed (optional)
    URL.revokeObjectURL(blobUrl);
} 

import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
const exportToXLSX = () => {
      const tabs = [
        {
          tabName: 'Sushi',
          data: reportSushi.value,
        },
        {
          tabName: 'Produce',
          data: reportProduce.value,
        },
        {
          tabName: 'Other',
          data: reportOther.value,
        },
      ];

      const workbook = XLSX.utils.book_new();

      tabs.forEach((tab) => {
        const data = [
          ['Item Name', 'Current Price', 'Quantity Order', 'Total Cost', 'Vendor Name', 'Ordering Channel', 'Contact Phone', 'Order Phone', 'Email'],
          ...tab.data.map((item) => [
            item.item_name,
            item.price,
            item.qty_ordered,
            item.total_cost,
            item.vendor_name,
            item.ordering_channel,
            item.contact_phone,
            item.order_phone,
            item.email,
          ]),
        ];

        const worksheet = XLSX.utils.aoa_to_sheet(data);
        XLSX.utils.book_append_sheet(workbook, worksheet, tab.tabName);
      });
      const dateTimeNow = new Date().toISOString().slice(0,-1);
      const xlsxWriteBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const fileName = 'Report_' + dateTimeNow + '_' + groupIDName.value + '.xlsx';
      const blob = new Blob([new Uint8Array(xlsxWriteBuffer)], { type: 'application/octet-stream' });
      saveAs(blob, fileName);
    };

function goToReportHistory(){
    router.push({name: 'ReportHistory'});
}
</script>
