import Api from '@/services/Api'

export default {
    //get Windows Username
    getWindowsUsername(){
        return Api().get('user');
    },
    //Login
    login(object){
        return Api().post('login', object);
    },
    //Forgot Password: Verify Email
    forgotPassword(email){
        return Api().post('forgotpassword', email);
    },
    //Reset Password: Verify Link ID
    verifyLink(link){
        return Api().get(`reset-password/get/${link}`);
    },
    //Reset Password: Send security response and new password
    resetPassword(item){
        return Api().post(`forgotpassword/answer`, item);
    },
    getState(){
        return Api().get('states');
    },
    //Get PRICE by Supply ID
    getPriceBySupplyID(supplyID){
        return Api().get(`price/${supplyID}`)
    },
    //SUPPLY
    //Get Supply
    getSupply(){
        return Api().get('supply/get-all');
    },
    //Get Item Type
    getItemType(){
        return Api().get('item-type/get-all');
    },
    //Add Supply
    addSupply(item, customHeader){
        return Api().post('supply/add', item, {
            headers: customHeader
        });
    },
    //Edit Supply
    editSupply(item, customHeader){
        return Api().put('supply/edit', item, {
            headers: customHeader
        });
    },
    //Delete Supply
    delSupply(supplyID, customHeader){
        return Api().delete(`supply/delete/${supplyID}`, {
            headers: customHeader
        });
    },
    //VENDOR
    //Get Vendors
    getVendor(){
        return Api().get('vendor/get-all');
    },        
    //Add Vendor
    addVendor(item, customHeader){
        return Api().post('vendor/add', item, {
            headers: customHeader
        });
    },
    //Edit Vendor
    editVendor(item, customHeader){
        return Api().put('vendor/edit', item, {
            headers: customHeader
        });
    },
    //Delete Vendor
    delVendor(vendorID, customHeader){
        return Api().delete(`vendor/delete/${vendorID}`, {
            headers: customHeader
        });
    },
    //ACCOUNT
    //Get Account Data
    getAccount(){
        return Api().get('account/get-all');
    },
    //Add Account
    addAccount(account, customHeader){
        return Api().post('account/add', account, {
            headers: customHeader
        });
    },
    //Edit Account
    editAccount(item, customHeader){
        return Api().put('account/edit', item, {
            headers: customHeader
        });
    },
    //Delete Vendor
    delAccount(acctID, customHeader){
        return Api().delete(`account/delete/${acctID}`, {
            headers: customHeader
        });
    },
    //ORDER
    //Update Order and Generate Report
    updateTransaction(item, customHeader){
        return Api().put(`order`, item, {
            headers: customHeader
        });
    }
}
