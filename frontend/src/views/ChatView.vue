<template>
  <div class="page-shell">
    <section class="hero section-card">
      <p class="section-tag">CHAT</p>
      <p class="kicker">LANGGRAPH CONVERSATION</p>
      <h1>智能对话</h1>
      <p class="sub-title">直接和潮韵云脑对话，咨询潮汕玩法、路线与文化建议。</p>
    </section>

    <section class="chat-shell glass-card">
      <div class="chat-list">
        <div
          v-for="(item, idx) in messages"
          :key="idx"
          class="chat-item"
          :class="item.role === 'user' ? 'chat-user' : 'chat-assistant'"
        >
          <p class="chat-role">{{ item.role === "user" ? "我" : "Agent" }}</p>
          <p class="chat-text">{{ item.content }}</p>
        </div>
        <p v-if="loading" class="sub-title">正在思考中...</p>
      </div>

      <form class="chat-input-row" @submit.prevent="submitChat">
        <input v-model="input" placeholder="比如：帮我规划一个潮州两日文化游" />
        <button class="neon-btn" type="submit" :disabled="loading || !input.trim()">
          {{ loading ? "发送中..." : "发送" }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { sendChat, type ChatMessage } from "../api/chat";

const input = ref("");
const loading = ref(false);
const messages = ref<ChatMessage[]>([
  {
    role: "assistant",
    content: "你好，我是潮韵云脑。你可以问我潮汕景点、美食路线、避坑建议或行程安排。",
  },
]);

async function submitChat() {
  const text = input.value.trim();
  if (!text || loading.value) return;

  const userMsg: ChatMessage = { role: "user", content: text };
  messages.value.push(userMsg);
  input.value = "";
  loading.value = true;

  let selectedModel = "";
  try {
    selectedModel = localStorage.getItem("chaoyun_selected_model") || "";
  } catch {
    selectedModel = "";
  }

  try {
    let profilePayload: {
      departure_city?: string;
      home_city?: string;
      preferences?: string[];
      food_preferences?: string[];
      budget_level?: string;
      note?: string;
    } = {};
    try {
      const cached = localStorage.getItem("chaoyun_profile");
      if (cached) {
        const profile = JSON.parse(cached) as {
          departureCity?: string;
          homeCity?: string;
          preferences?: string[];
          foodPreferences?: string[];
          budgetLevel?: string;
          note?: string;
        };
        profilePayload = {
          departure_city: profile.departureCity ?? "",
          home_city: profile.homeCity ?? "",
          preferences: profile.preferences ?? [],
          food_preferences: profile.foodPreferences ?? [],
          budget_level: profile.budgetLevel ?? "",
          note: profile.note ?? "",
        };
      }
    } catch {
      profilePayload = {};
    }

    const resp = await sendChat({
      message: text,
      history: messages.value.slice(-12),
      model: selectedModel || undefined,
      user_id: "default",
      user_profile: profilePayload,
    });
    messages.value.push({
      role: "assistant",
      content: `${resp.reply}\n\n（模型：${resp.model_used}）`,
    });
  } catch (err) {
    messages.value.push({
      role: "assistant",
      content: err instanceof Error ? `请求失败：${err.message}` : "请求失败，请稍后重试",
    });
  } finally {
    loading.value = false;
  }
}
</script>
