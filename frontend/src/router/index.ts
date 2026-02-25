import { createRouter, createWebHistory } from "vue-router";

import ChatView from "../views/ChatView.vue";
import PlannerView from "../views/PlannerView.vue";
import ProfileView from "../views/ProfileView.vue";
import ChaoshanView from "../views/ChaoshanView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "chat", component: ChatView },
    { path: "/planner", name: "planner", component: PlannerView },
    { path: "/profile", name: "profile", component: ProfileView },
    { path: "/chaoshan", name: "chaoshan", component: ChaoshanView },
  ],
});

export default router;
