import Api from '@/services/Api'

export default {
    //get Windows Username
    getWindowsUsername(){
        return Api().get('user');
    }    
}