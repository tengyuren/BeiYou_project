import {createRouter, createWebHashHistory} from "vue-router";
import Home from "../views/Home.vue";

const routes = [
    {
        path: '/',
        redirect: '/dashboard'
    }, {
        path: "/",
        name: "Home",
        component: Home,
        children: [
            {
                path: "/dashboard",
                name: "dashboard",
                meta: {
                    role:["admin","user"],
                    title: '系统首页'
                },
                component: () => import ( /* webpackChunkName: "dashboard" */ "../views/Dashboard.vue")
            }, {
                path: "/usermanag",
                name: "usermanag",
                meta: {
                    role:["admin"],
                    title: '用户管理'
                },
                component: () => import ( /* webpackChunkName: "table" */ "../views/Usermanag.vue")
            }, {
                path: "/scene",
                name: "scene",
                meta: {
                    title: '场景管理'
                },
                component: () => import ( /* webpackChunkName: "tabs" */ "../views/Scene.vue")
            },{
                path: '/pereditor',
                name: 'editor',
                meta: {
                    title: '用户权限'
                },
                component: () => import (/* webpackChunkName: "editor" */ '../views/Pereditor.vue')
            },{
                path: '/403',
                name: '403',
                meta: {
                    title: '没有权限'
                },
                component: () => import (/* webpackChunkName: "403" */ '../views/403.vue')
            },{
                path: '/user',
                name: 'user',
                meta: {
                    title: '个人中心'
                },
                component: () => import (/* webpackChunkName: "user" */ '../views/User.vue')
            },{
                path: "/permission",
                name: "permission",
                meta: {
                    title: '权限错误',
                    permission: true
                },
                component: () => import ( /* webpackChunkName: "permission" */ "../views/Permission.vue")
            }, {
                path: "/message",
                name: "message",
                meta: {
                    title: '消息提醒'
                },
                component: () => import ( /* webpackChunkName: "form" */ "../views/Message.vue")
            },{
                path: "/i18n",
                name: "i18n",
                meta: {
                    title: '国际化语言'
                },
                component: () => import ( /* webpackChunkName: "i18n" */ "../views/I18n.vue")
            }, {
                path: "/charts",
                name: "charts",
                meta: {
                    title: '数据图表'
                },
                component: () => import ( /* webpackChunkName: "upload" */ "../views/Charts.vue")
            }, {
                path: "/datacenter",
                name: "datacenter",
                meta: {
                    title: '数据计算'
                },
                component: () => import ( /* webpackChunkName: "icon" */ "../views/DataComp.vue")
            }, {
                path: '/404',
                name: '404',
                meta: {
                    title: '找不到页面'
                },
                component: () => import (/* webpackChunkName: "404" */ '../views/404.vue')
            },
            {
                path: '/icon',
                name: 'icon',
                meta: {
                    title: '图标'
                },
                component: () => import (/* webpackChunkName: "404" */ '../views/Icon.vue')
            },
        ]
    }, {
        path: "/login",
        name: "Login",
        meta: {
            title: '登录'
        },
        component: () => import ( /* webpackChunkName: "login" */ "../views/Login.vue")
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title}`;
    const role = localStorage.getItem('ms_username');
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permission) {
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin'
            ? next()
            : next('/403');
    } else {
        next();
    }
});

export default router;