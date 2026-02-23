<template>
  <main>
    <header class="top-nav">
      <div class="top-nav-inner">
        <RouterLink to="/" class="brand">
          <span class="brand-mark" aria-hidden="true"></span>
          <span>潮韵云脑</span>
        </RouterLink>
        <nav class="nav-links" aria-label="主导航">
          <RouterLink to="/">行程规划</RouterLink>
          <RouterLink to="/profile">我的信息</RouterLink>
          <div class="model-dropdown-wrap">
            <button class="model-trigger" type="button" @click="toggleModelMenu">
              {{ currentModel.label }}
              <span class="model-arrow" :class="{ open: modelMenuOpen }">⌃</span>
            </button>
            <transition name="slide-down">
              <div v-if="modelMenuOpen" class="model-menu">
                <button
                  v-for="item in modelOptions"
                  :key="item.value"
                  class="model-option"
                  type="button"
                  @click="selectModel(item.value)"
                >
                  <div>
                    <p class="model-option-title">{{ item.label }}</p>
                    <p class="model-option-desc">{{ item.desc }}</p>
                  </div>
                  <span v-if="item.value === selectedModel" class="model-check">✓</span>
                </button>
              </div>
            </transition>
          </div>
          <RouterLink to="/chaoshan">走进潮汕</RouterLink>
          <a href="https://github.com/Hurvin/GEEKDAY" target="_blank" rel="noreferrer">GitHub</a>
        </nav>
      </div>
    </header>
    <section class="content-shell">
      <RouterView />
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { fetchModels, type ModelOption } from "./api/planner";

const fallbackOptions: ModelOption[] = [
  { value: "Qwen2.5-72B-Instruct", label: "Qwen2.5-72B", desc: "综合能力强，适合旅行规划与生成" },
  { value: "DeepSeek-V3", label: "DeepSeek-V3", desc: "推理与代码能力均衡，适合复杂任务" },
  { value: "DeepSeek-R1", label: "DeepSeek-R1", desc: "强化推理链路，适合深度思考" },
  { value: "Hunyuan-TurboS", label: "Hunyuan", desc: "通用处理与长文本理解表现稳定" },
];
const modelOptions = ref<ModelOption[]>(fallbackOptions);
const selectedModel = ref<string>(fallbackOptions[0].value);
const modelMenuOpen = ref(false);

const currentModel = computed(
  () => modelOptions.value.find((item) => item.value === selectedModel.value) ?? modelOptions.value[0]
);

function toggleModelMenu() {
  modelMenuOpen.value = !modelMenuOpen.value;
}

function selectModel(value: string) {
  selectedModel.value = value;
  modelMenuOpen.value = false;
  try {
    localStorage.setItem("chaoyun_selected_model", value);
  } catch {
    // 忽略 localStorage 不可用场景
  }
}

try {
  const saved = localStorage.getItem("chaoyun_selected_model");
  if (saved && modelOptions.value.some((item) => item.value === saved)) {
    selectedModel.value = saved;
  }
} catch {
  // 忽略 localStorage 不可用场景
}

onMounted(async () => {
  try {
    const remoteOptions = await fetchModels();
    if (remoteOptions.length > 0) {
      modelOptions.value = remoteOptions;
      if (!remoteOptions.some((item) => item.value === selectedModel.value)) {
        selectedModel.value = remoteOptions[0].value;
      }
    }
  } catch {
    modelOptions.value = fallbackOptions;
  }
});
</script>
