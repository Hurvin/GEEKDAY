<template>
  <div class="page-shell">
    <section class="hero section-card">
      <p class="section-tag">PREVIEW</p>
      <p class="kicker">23.5°N CHAOSHAN INTEL TRIP AGENT</p>
      <h1>潮韵同行</h1>
      <p class="sub-title">用动态规划，触碰潮汕文旅认知边界</p>
    </section>

    <section class="panel-grid">
      <PlannerForm :loading="loading" @submit="onSubmit" />
      <ResultPanel :result="result" :loading="loading" :error="error" :stage="stage" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import PlannerForm from "../components/PlannerForm.vue";
import ResultPanel from "../components/ResultPanel.vue";
import { createPlan, type PlanPayload, type PlanResult } from "../api/planner";

const loading = ref(false);
const error = ref("");
const result = ref<PlanResult | null>(null);
const stage = ref<"idle" | "loading" | "partial" | "final" | "error">("idle");

async function onSubmit(payload: PlanPayload) {
  loading.value = true;
  error.value = "";
  stage.value = "loading";
  let selectedModel = "";
  try {
    selectedModel = localStorage.getItem("chaoyun_selected_model") || "";
  } catch {
    selectedModel = "";
  }
  const partialTimer = setTimeout(() => {
    if (loading.value) {
      stage.value = "partial";
    }
  }, 700);
  try {
    result.value = await createPlan({
      ...payload,
      model: selectedModel || undefined,
    });
    stage.value = "final";
  } catch (err) {
    error.value = err instanceof Error ? err.message : "请求失败，请重试";
    stage.value = "error";
  } finally {
    clearTimeout(partialTimer);
    loading.value = false;
  }
}
</script>
