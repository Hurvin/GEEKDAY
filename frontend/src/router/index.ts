import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import ProfileView from "../views/ProfileView.vue";
import ChaoshanView from "../views/ChaoshanView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/profile", name: "profile", component: ProfileView },
    { path: "/chaoshan", name: "chaoshan", component: ChaoshanView },
  ],
});

export default router;
