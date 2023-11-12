import { createRouter, createWebHistory } from 'vue-router';
import { useAppStore } from '@/store/app';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }, // Add a meta field to indicate that authentication is required
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/supply',
    name: 'Supply',
    component: () => import('@/components/Supply.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/vendor',
    name: 'Vendor',
    component: () => import('@/components/Vendor.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/account',
    name: 'Account',
    component: () => import('@/components/Account.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('@/components/Order.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/report-history',
    name: 'ReportHistory',
    component: () => import('@/components/ReportHistory.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('@/views/ResetPassword.vue'),
    beforeEnter: (to, from, next) => {
      if (to.query.id) {
        console.log(to.query.id);
        // If 'id' query parameter is present, allow the navigation to the ResetPassword view
        next();
      } else {
        // If 'id' query parameter is not present, redirect to the login page
        next({ name: 'Login' });
      }
    },
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Add a global navigation guard
router.beforeEach((to, from, next) => {
  const piniaStore = useAppStore(); // Create an instance of your store
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Check if the route requires authentication
    if (piniaStore.loginSuccess || sessionStorage.getItem('loginSuccess') === 'true') {
      // If loginSuccess is true, allow the navigation
      next();
    } else if (to.name !== 'Login') {
      // If not authenticated and not already on the login page, redirect to the login page
      next({ name: 'Login' });
    } /* else if(to.name === 'ResetPassword' && to.query.id) {
      next({ name: 'ResetPassword', params: {id: to.query.id}});
    } */
    else {
      // Otherwise, allow the navigation to the login page
      next();
    }
  } else {
    // For routes that do not require authentication, allow the navigation
    next();
  }
});

export default router;
