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
        return Api().post('forgot-password', email);
    },
    //Role Check
    checkRole(){
        return Api().get('rolecheck');
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
    addSupply(item){
        return Api().post('', item);
    },
    //Edit Supply
    editSupply(item){
        return Api().put('', item);
    },
    //Delete Supply
    delSupply(item){
        return Api().delete('');
    },
    //VENDOR
    //Get Vendors
    getVendor(){
        return Api().get('vendor/get-all');
    },        
    //Add Vendor
    addVendor(item){
        return Api().post('vendor/add', item);
    },
    //Edit Vendor
    editVendor(item){
        return Api().put('', item);
    },
    //Delete Vendor
    delVendor(item){
        return Api().delete('');
    },
    //ACCOUNT
    //Get Account Data
    getAccount(){
        return Api().get('account/get-all');
    },
    //Add Account
    addAccount(account){
        return Api().post('account/add', account);
    },
    //Edit Account
    editAccount(item){
        return Api().put('', item);
    },
    //Delete Vendor
    delAccount(item){
        return Api().delete('');
    }
}