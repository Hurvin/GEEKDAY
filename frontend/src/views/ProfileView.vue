<template>
  <div class="page-shell">
    <section class="section-card">
      <p class="section-tag">PROFILE</p>
      <h1>我的旅行信息</h1>
      <p class="sub-title">设置你的基础信息和偏好，帮助 Agent 给出更贴合你的行程。</p>
    </section>

    <form class="glass-card form" @submit.prevent="saveProfile">
      <label>
        出发城市
        <input v-model="profile.departureCity" />
      </label>
      <label>
        常住城市
        <input v-model="profile.homeCity" />
      </label>
      <label>
        出行偏好（逗号分隔）
        <input v-model="preferencesText" />
      </label>
      <label>
        饮食偏好（逗号分隔）
        <input v-model="foodText" />
      </label>
      <label>
        预算偏好
        <select v-model="profile.budgetLevel">
          <option value="经济">经济</option>
          <option value="中等">中等</option>
          <option value="品质">品质</option>
        </select>
      </label>
      <label>
        备注
        <input v-model="profile.note" />
      </label>
      <button class="neon-btn" type="submit">保存我的信息</button>
      <p v-if="saved" class="sub-title">已保存，下次打开会自动恢复。</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

type ProfileData = {
  departureCity: string;
  homeCity: string;
  preferences: string[];
  foodPreferences: string[];
  budgetLevel: string;
  note: string;
};

const profile = reactive<ProfileData>({
  departureCity: "",
  homeCity: "潮汕",
  preferences: [],
  foodPreferences: [],
  budgetLevel: "中等",
  note: "",
});

const preferencesText = ref("");
const foodText = ref("");
const saved = ref(false);

function splitValues(text: string): string[] {
  return text
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function saveProfile() {
  profile.preferences = splitValues(preferencesText.value);
  profile.foodPreferences = splitValues(foodText.value);
  localStorage.setItem("chaoyun_profile", JSON.stringify(profile));
  saved.value = true;
}

const cached = localStorage.getItem("chaoyun_profile");
if (cached) {
  const parsed = JSON.parse(cached) as ProfileData;
  profile.departureCity = parsed.departureCity ?? "";
  profile.homeCity = parsed.homeCity ?? "潮汕";
  profile.preferences = parsed.preferences ?? [];
  profile.foodPreferences = parsed.foodPreferences ?? [];
  profile.budgetLevel = parsed.budgetLevel ?? "中等";
  profile.note = parsed.note ?? "";
  preferencesText.value = profile.preferences.join(",");
  foodText.value = profile.foodPreferences.join(",");
}
</script>
