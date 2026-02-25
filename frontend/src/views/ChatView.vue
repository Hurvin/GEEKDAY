<template>
  <div class="page-shell">
    <section class="hero section-card">
      <p class="section-tag">CHAT</p>
      <p class="kicker">LANGGRAPH CONVERSATION</p>
      <h1>智能对话</h1>
      <p class="sub-title">直接和潮韵同行对话，咨询潮汕玩法、路线与文化建议。</p>
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
          <p class="chat-text">
            <template v-for="(segment, sIdx) in parseContent(item.content)" :key="sIdx">
              <SpotTooltip 
                v-if="segment.type === 'spot'" 
                :name="segment.text" 
              />
              <span v-else>{{ segment.text }}</span>
        </template>
      </p>
    </div>
    
    <!-- AI Thinking Indicator -->
    <div v-if="loading" class="chat-item chat-assistant">
      <p class="chat-role">Agent</p>
      <div class="chat-thinking">
        <img src="/jz.gif" alt="Thinking..." class="thinking-gif" />
        <span class="thinking-text">正在思考中...</span>
      </div>
    </div>
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
import SpotTooltip from "../components/SpotTooltip.vue";
import { spotKeywords } from "../data/spots";

const input = ref("");
const loading = ref(false);
const messages = ref<ChatMessage[]>([
  {
    role: "assistant",
    content: "你好，我是潮韵同行。你可以问我潮汕景点、美食路线、避坑建议或行程安排。",
  },
]);

function parseContent(content: string) {
  if (!content) return [{ type: 'text', text: '' }];
  
  // Sort keywords by length descending to match longest first
  const sortedKeywords = [...spotKeywords].sort((a, b) => b.length - a.length);
  const regex = new RegExp(`(${sortedKeywords.join('|')})`, 'g');
  
  return content.split(regex).map(part => {
    if (spotKeywords.includes(part)) {
      return { type: 'spot', text: part };
    }
    return { type: 'text', text: part };
  });
}

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

<style scoped>
.chat-list {
  overflow-y: auto;
  margin-bottom: 20px;
}

.chat-item {
  margin-bottom: 12px;
}

.chat-user {
  text-align: right;
}

.chat-assistant {
  text-align: left;
}

.chat-role {
  font-size: 0.8rem;
  color: var(--text-sub);
  margin-bottom: 4px;
}

.chat-thinking {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.05);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(110, 141, 255, 0.2);
}

.thinking-gif {
  height: 40px;
  width: auto;
  border-radius: 4px;
}

.thinking-text {
  color: var(--text-sub);
  font-size: 0.9rem;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.chat-text {
  display: inline-block;
  background: rgba(255, 255, 255, 0.08);
  padding: 10px 14px;
  border-radius: 8px;
  line-height: 1.5;
  color: var(--text-main);
  max-width: 80%;
  text-align: left;
  white-space: pre-wrap;
}

.chat-user .chat-text {
  background: rgba(78, 245, 214, 0.15);
  color: #fff;
}
</style>
