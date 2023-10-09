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
    }
}