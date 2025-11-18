import { createRouter, createWebHistory } from 'vue-router'

// 路由懶加載
const Home = () => import('@/views/Home.vue')
const Login = () => import('@/views/Login.vue')
const Register = () => import('@/views/Register.vue')
const ForgotPassword = () => import('@/views/ForgotPassword.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const Activities = () => import('@/views/Activities.vue')
const ActivityDetail = () => import('@/views/ActivityDetail.vue')
const Matches = () => import('@/views/Matches.vue')
const Chat = () => import('@/views/Chat.vue')
const Profile = () => import('@/views/Profile.vue')
const UserProfile = () => import('@/views/user/UserProfile.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'EdgeSurvivor - 邊緣人神器'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '登入 - EdgeSurvivor'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '註冊 - EdgeSurvivor'
    }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: {
      title: '忘記密碼 - EdgeSurvivor'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '控制台 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/activities',
    name: 'Activities',
    component: Activities,
    meta: {
      title: '活動管理 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/activities/:id',
    name: 'ActivityDetail',
    component: ActivityDetail,
    meta: {
      title: '活動詳情 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/matches',
    name: 'Matches',
    component: Matches,
    meta: {
      title: '旅伴交友 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: {
      title: '聊天 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      title: '個人資料 - EdgeSurvivor',
      requiresAuth: true
    }
  },
  {
    path: '/user/:id',
    name: 'UserProfile',
    component: UserProfile,
    meta: {
      title: '用戶資料 - EdgeSurvivor',
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守衛 - 檢查認證
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    // 需要認證但沒有 token，跳轉到登入頁
    next('/login')
  } else if (to.path === '/login' && token) {
    // 已登入用戶訪問登入頁，跳轉到控制台
    next('/dashboard')
  } else {
    next()
  }
})

export default router