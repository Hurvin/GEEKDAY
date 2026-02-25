<template>
  <form class="glass-card form" @submit.prevent="submitForm">
    <h2>行程输入</h2>
    
    <!-- 基本信息 -->
    <div class="form-section">
      <h3>基本信息</h3>
      <div class="grid-2">
        <label>
          目的地
          <input v-model="form.destination" placeholder="例如：汕头、潮州" required />
        </label>
        <label>
          天数
          <input v-model.number="form.days" type="number" min="1" max="7" />
        </label>
      </div>
      <div class="grid-2">
        <label>
          出发日期 (可选)
          <input type="date" v-model="form.start_date" :min="minDate" />
        </label>
        <label>
          出游风格
          <select v-model="form.travel_style">
            <option>轻松休闲</option>
            <option>文化深度</option>
            <option>美食特种兵</option>
            <option>网红打卡</option>
          </select>
        </label>
      </div>
      <div class="grid-2">
        <label>
          同行人群
          <select v-model="form.travelers">
            <option>独自一人</option>
            <option>情侣/夫妻</option>
            <option>朋友结伴</option>
            <option>亲子家庭</option>
            <option>带父母长辈</option>
          </select>
        </label>
      </div>
    </div>

    <!-- 衣食住行 -->
    <div class="form-section">
      <h3>衣食住行偏好</h3>
      
      <!-- 衣 -->
      <label>
        👗 穿搭风格 (衣)
        <select v-model="form.clothing_style">
          <option>休闲舒适 (以走路为主)</option>
          <option>出片穿搭 (适合拍照)</option>
          <option>汉服/国风 (古城适配)</option>
          <option>清凉海岛 (南澳适配)</option>
        </select>
      </label>

      <!-- 食 -->
      <label>
        🍜 饮食偏好 (食 - 多选)
        <div class="checkbox-group">
          <label v-for="opt in foodOptions" :key="opt">
            <input type="checkbox" :value="opt" v-model="form.food_preference">
            {{ opt }}
          </label>
        </div>
      </label>

      <!-- 住 -->
      <label>
        🏨 住宿类型 (住)
        <select v-model="form.accommodation_type">
          <option>经济型酒店 (性价比)</option>
          <option>特色民宿 (体验当地风情)</option>
          <option>高档酒店 (舒适服务)</option>
          <option>青旅 (结交朋友)</option>
        </select>
      </label>

      <!-- 行 -->
      <label>
        🚗 交通方式 (行)
        <select v-model="form.transport_preference">
          <option>网约车/出租车</option>
          <option>自驾/租车</option>
          <option>公交/共享电单车</option>
          <option>包车游</option>
        </select>
      </label>
    </div>

    <!-- 补充信息 -->
    <div class="form-section">
      <h3>补充需求</h3>
      
      <div v-if="availableCompanions.length > 0" class="companions-selection">
        <label>选择同行人员 (从我的档案)</label>
        <div class="checkbox-group">
          <label v-for="person in availableCompanions" :key="person.name">
            <input 
              type="checkbox" 
              :value="person" 
              v-model="selectedCompanions"
            >
            {{ person.name }} ({{ person.relation }})
          </label>
        </div>
      </div>

      <label>
        其他偏好
        <input v-model="preferencesText" placeholder="例如：想看日出、对海鲜过敏..." />
      </label>
    </div>

    <button class="neon-btn submit-btn" :disabled="loading" type="submit">
      {{ loading ? "生成中..." : "生成动态行程" }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import type { PlanPayload } from "../api/planner";

defineProps<{ loading: boolean }>();
const emit = defineEmits<{ submit: [payload: PlanPayload] }>();

const foodOptions = ["牛肉火锅", "生腌", "卤鹅", "肠粉/粿条", "功夫茶", "甜汤", "深夜大排档"];

const form = reactive<PlanPayload & {
  food_preference: string[];
  clothing_style: string;
  accommodation_type: string;
  transport_preference: string;
  start_date: string;
}>({
  destination: "汕头",
  days: 2,
  travel_style: "美食特种兵",
  travelers: "朋友结伴",
  preferences: [],
  constraints: [],
  budget_level: "中等",
  // New fields defaults
  clothing_style: "休闲舒适 (以走路为主)",
  food_preference: ["牛肉火锅", "肠粉/粿条"],
  accommodation_type: "经济型酒店 (性价比)",
  transport_preference: "网约车/出租车",
  start_date: "",
});

const minDate = new Date().toISOString().split('T')[0];
const preferencesText = ref("");

// Companions
const availableCompanions = ref<any[]>([]);
const selectedCompanions = ref<any[]>([]);

onMounted(() => {
  try {
    const cached = localStorage.getItem("chaoyun_profile");
    if (cached) {
      const profile = JSON.parse(cached);
      if (profile.companions && Array.isArray(profile.companions)) {
        availableCompanions.value = profile.companions;
      }
      
      // Auto-fill form defaults from profile
      if (profile.clothingStyle) form.clothing_style = profile.clothingStyle;
      if (profile.foodPreferences) form.food_preference = profile.foodPreferences;
      if (profile.accommodationType) form.accommodation_type = profile.accommodationType;
      if (profile.transportPreference) form.transport_preference = profile.transportPreference;
      if (profile.budgetLevel) form.budget_level = profile.budgetLevel;
    }
  } catch (e) {
    console.error("Failed to load profile", e);
  }
});

function submitForm() {
  // Combine all preferences into the main array for backend compatibility
  const combinedPreferences = [
    ...form.food_preference.map(f => `想吃${f}`),
    `穿搭偏好：${form.clothing_style}`,
    `住宿偏好：${form.accommodation_type}`,
    `交通偏好：${form.transport_preference}`,
    ...splitValues(preferencesText.value)
  ];
  
  if (form.start_date) {
    combinedPreferences.push(`出发日期：${form.start_date}`);
  }

  emit("submit", {
    ...form,
    preferences: combinedPreferences,
    constraints: [], // Constraints can be handled in text if needed
    companions: selectedCompanions.value,
    start_date: form.start_date,
  });
}

function splitValues(text: string): string[] {
  return text
    .split(/[,，]/) // Support both EN and CN commas
    .map((item) => item.trim())
    .filter(Boolean);
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
}

h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 12px;
}

h3 {
  font-size: 1rem;
  color: var(--accent);
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--text-sub);
}

input, select {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(110, 141, 255, 0.2);
  border-radius: 4px;
  padding: 8px 12px;
  color: var(--text-main);
  font-size: 0.95rem;
  transition: all 0.2s;
}

input:focus, select:focus {
  border-color: var(--accent);
  outline: none;
  background: rgba(0, 0, 0, 0.4);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-group label {
  flex-direction: row;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.05);
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.checkbox-group label:has(input:checked) {
  background: rgba(78, 245, 214, 0.15);
  border-color: rgba(78, 245, 214, 0.4);
  color: var(--accent);
}

.companions-selection {
  margin-bottom: 16px;
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 8px;
}

.companions-selection label {
  margin-bottom: 8px;
  font-weight: bold;
}
.submit-btn {
  margin-top: 12px;
  width: 100%;
  justify-content: center;
  font-size: 1rem;
  padding: 12px;
}
</style>
