<template>
  <form class="glass-card form" @submit.prevent="submitForm">
    <h2>行程输入</h2>
    <label>
      目的地
      <input v-model="form.destination" required />
    </label>
    <label>
      天数
      <input v-model.number="form.days" type="number" min="1" max="7" />
    </label>
    <label>
      出游风格
      <select v-model="form.travel_style">
        <option>轻松</option>
        <option>紧凑</option>
        <option>特种兵</option>
      </select>
    </label>
    <label>
      同行人群
      <input v-model="form.travelers" />
    </label>
    <label>
      偏好（逗号分隔）
      <input v-model="preferencesText" />
    </label>
    <label>
      约束（逗号分隔）
      <input v-model="constraintsText" />
    </label>
    <button class="neon-btn" :disabled="loading" type="submit">
      {{ loading ? "生成中..." : "生成动态行程" }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import type { PlanPayload } from "../api/planner";

defineProps<{ loading: boolean }>();
const emit = defineEmits<{ submit: [payload: PlanPayload] }>();

const form = reactive<PlanPayload>({
  destination: "汕头",
  days: 2,
  travel_style: "轻松",
  travelers: "朋友",
  preferences: ["美食", "文化体验"],
  constraints: ["不赶路"],
  budget_level: "中等",
});

const preferencesText = ref(form.preferences.join(","));
const constraintsText = ref(form.constraints.join(","));

function splitValues(text: string): string[] {
  return text
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function submitForm() {
  emit("submit", {
    ...form,
    preferences: splitValues(preferencesText.value),
    constraints: splitValues(constraintsText.value),
  });
}
</script>
