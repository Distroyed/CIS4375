// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    isLoading: false,
    noData: false,
    showSnackBar: false,
    catchError: null,
    isSuccess: null,
    currentUser: '',    
    currentUserName: '',
    currentRole: '',
    currentFName: '',
    currentLName: '',
    loginSuccess: false,
    forgotPW: false
  }),
  //getter - simiiliar to computed property, getting will change when data changed
  getters: {
    //count: state => state.duplicateDealData.length
    getLoginSuccess() {
      return this.loginSuccess;
    },
  },
  //action used to modify properties in state management
  actions: {
    initializeUserData(currentUserName, currentUser, currentRole, loginSuccess) {
      this.loginSuccess = loginSuccess;
      this.currentRole = currentRole;
      this.currentUserName = currentUserName;
      this.currentUser = currentUser
    },
    // Set authentication status and user data
    setAuthenticationStatus({ loginSuccess, currentRole, currentUserName, currentUser }) {
      this.loginSuccess = loginSuccess;
      this.currentRole = currentRole;
      this.currentUserName = currentUserName;
      this.currentUser = currentUser
      // Store authentication-related data in session storage
      if (loginSuccess) {
        sessionStorage.setItem('loginSuccess', 'true');
        sessionStorage.setItem('currentRole', currentRole);
        sessionStorage.setItem('currentUserName', currentUserName);
        sessionStorage.setItem('currentUser', currentUser);
      } else {
        sessionStorage.removeItem('loginSuccess');
        sessionStorage.removeItem('currentRole');
        sessionStorage.removeItem('currentUserName');
        sessionStorage.removeItem('currentUser');
      }
    },
    // Clear authentication status and user data
    clearAuthenticationStatus() {
      this.loginSuccess = false;
      this.currentRole = '';
      this.currentUserName = '';

      // Remove authentication-related data from session storage
      sessionStorage.removeItem('loginSuccess');
      sessionStorage.removeItem('currentRole');
      sessionStorage.removeItem('currentUserName');
      sessionStorage.removeItem('currentUser');
    },
    setSnackBar (catchError, isSuccess) {
      this.isSuccess = isSuccess
      this.showSnackBar = true
      this.catchError = catchError
      setTimeout(() => {this.showSnackBarError = false, this.catchError = null}, 4000)
    }
  }
})
