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
    setSnackBar (catchError, isSuccess) {
      this.isSuccess = isSuccess
      this.showSnackBar = true
      this.catchError = catchError
      setTimeout(() => {this.showSnackBarError = false, this.catchError = null}, 4000)
    }
  }
})
