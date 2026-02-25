<template>
  <div class="page-shell">
    <section class="hero section-card">
      <p class="section-tag">CHAT</p>
      <p class="kicker">LANGGRAPH CONVERSATION</p>
      <h1>智能对话</h1>
      <p class="sub-title">直接和潮韵同行对话，咨询潮汕玩法、路线与文化建议。</p>
      <div v-if="mcpServices.length > 0" class="mcp-services">
        <p class="mcp-title">支持 MCP 服务：</p>
        <span 
          v-for="service in mcpServices" 
          :key="service.name" 
          class="mcp-chip" 
          :title="service.name"
          @click="openMcpDialog(service)"
        >
          {{ service.description }}
        </span>
      </div>
    </section>

    <!-- MCP Parameter Dialog -->
    <div v-if="showMcpDialog && selectedMcpService" class="loading-modal" @click.self="closeMcpDialog">
      <div class="mcp-modal-content">
        <h3>使用 {{ selectedMcpService.description }}</h3>
        <p class="mcp-modal-desc">请输入以下参数：</p>
        
        <div class="mcp-form">
          <div v-for="param in selectedMcpService.parameters" :key="param.name" class="mcp-field">
            <label>
              {{ param.description }}
              <span v-if="param.required" class="required">*</span>
            </label>
            <input 
              v-model="mcpParams[param.name]" 
              :placeholder="'请输入 ' + param.description"
              @keyup.enter="submitMcpParams"
            />
          </div>
        </div>

        <div class="mcp-actions">
          <button class="neon-btn secondary" @click="closeMcpDialog">取消</button>
          <button class="neon-btn" @click="submitMcpParams">确认使用</button>
        </div>
      </div>
    </div>

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
    
  </div>

  <form class="chat-input-row" @submit.prevent="submitChat">
        <input v-model="input" placeholder="比如：帮我规划一个潮州两日文化游" />
        <button class="neon-btn" type="submit" :disabled="loading || !input.trim()">
          {{ loading ? "发送中..." : "发送" }}
        </button>
      </form>
    </section>

    <div v-if="loading" class="loading-modal" role="status" aria-live="polite" aria-label="模型回复中">
      <div class="loading-modal-content">
        <img src="/jz.gif" alt="模型思考中" class="loading-modal-gif" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchMcpServices, sendChat, type ChatMessage, type McpServiceItem } from "../api/chat";
import SpotTooltip from "../components/SpotTooltip.vue";
import { spotKeywords } from "../data/spots";

const input = ref("");
const loading = ref(false);
const mcpServices = ref<McpServiceItem[]>([]);
const showMcpDialog = ref(false);
const selectedMcpService = ref<McpServiceItem | null>(null);
const mcpParams = ref<Record<string, string>>({});

const messages = ref<ChatMessage[]>([
  {
    role: "assistant",
    content: "你好，我是潮韵同行。你可以问我潮汕景点、美食路线、避坑建议或行程安排。",
  },
]);

function openMcpDialog(service: McpServiceItem) {
  selectedMcpService.value = service;
  const newParams: Record<string, string> = {};
  if (service.parameters) {
    service.parameters.forEach(p => {
      newParams[p.name] = "";
    });
  }
  mcpParams.value = newParams;
  showMcpDialog.value = true;
}

function closeMcpDialog() {
  showMcpDialog.value = false;
  selectedMcpService.value = null;
}

function submitMcpParams() {
  if (!selectedMcpService.value) return;
  
  const serviceName = selectedMcpService.value.name;
  const serviceDesc = selectedMcpService.value.description;
  
  // Construct prompt
  let prompt = `请调用工具 ${serviceName} (${serviceDesc})，参数如下：\n`;
  let hasParams = false;
  
  for (const param of selectedMcpService.value.parameters || []) {
    const val = mcpParams.value[param.name];
    if (val && val.trim()) {
      prompt += `- ${param.name}: ${val}\n`;
      hasParams = true;
    } else if (param.required) {
      alert(`请输入${param.description}`);
      return;
    }
  }
  
  input.value = prompt;
  closeMcpDialog();
}

onMounted(async () => {
  try {
    mcpServices.value = await fetchMcpServices();
  } catch {
    mcpServices.value = [];
  }
});

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
      companions?: any[];
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
          companions?: any[];
        };
        profilePayload = {
          departure_city: profile.departureCity ?? "",
          home_city: profile.homeCity ?? "",
          preferences: profile.preferences ?? [],
          food_preferences: profile.foodPreferences ?? [],
          budget_level: profile.budgetLevel ?? "",
          note: profile.note ?? "",
          companions: profile.companions ?? [],
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

.mcp-services {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  align-items: center;
}

.mcp-title {
  margin: 0;
  color: var(--text-sub);
  font-size: 0.9rem;
}

.mcp-chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(141, 161, 255, 0.35);
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-main);
  font-size: 0.82rem;
}

.loading-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.55);
}

.loading-modal-content {
  padding: 16px;
  border-radius: 12px;
  background: rgba(14, 23, 56, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.loading-modal-gif {
  display: block;
  width: min(60vw, 360px);
  height: auto;
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

.mcp-chip {
  cursor: pointer;
  transition: all 0.2s;
}

.mcp-chip:hover {
  background: rgba(141, 161, 255, 0.15);
  transform: translateY(-1px);
}

.mcp-modal-content {
  padding: 24px;
  border-radius: 16px;
  background: rgba(14, 23, 56, 0.95);
  border: 1px solid rgba(78, 245, 214, 0.4);
  width: min(400px, 90vw);
  box-shadow: 0 0 40px rgba(0,0,0,0.5);
  animation: slide-up 0.3s ease-out;
}

.mcp-modal-content h3 {
  margin: 0 0 10px;
  color: #fff;
  font-size: 1.2rem;
}

.mcp-modal-desc {
  color: var(--text-sub);
  margin-bottom: 20px;
  font-size: 0.9rem;
}

.mcp-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.mcp-field label {
  display: block;
  margin-bottom: 6px;
  color: var(--text-main);
  font-size: 0.9rem;
}

.mcp-field .required {
  color: #ff6b6b;
  margin-left: 4px;
}

.mcp-field input {
  width: 100%;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #fff;
  font-size: 0.95rem;
}

.mcp-field input:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.1);
}

.mcp-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
