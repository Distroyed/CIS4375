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
    //meta: { requiresAuth: true },
  },
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
    if (piniaStore.loginSuccess) {
      // If loginSuccess is true, allow the navigation
      next();
    } else if (to.name !== 'Login') {
      // If not authenticated and not already on the login page, redirect to the login page
      next({ name: 'Login' });
    } else {
      // Otherwise, allow the navigation to the login page
      next();
    }
  } else {
    // For routes that do not require authentication, allow the navigation
    next();
  }
});

export default router;
