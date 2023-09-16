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
    } else {
      // If not authenticated, redirect to the login page
      next({ name: 'Login' });
    }
  } else {
    // For routes that do not require authentication, allow the navigation
    next();
  }
});

export default router;
