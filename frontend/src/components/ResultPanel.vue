<template>
  <section class="glass-card result">
    <h2>Agent 输出</h2>
    <p v-if="loading && stage === 'loading'">正在接收需求并启动动态规划...</p>
    <p v-else-if="loading && stage === 'partial'">已获取部分信号，正在整合文化规则与避坑策略...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!result">提交需求后将展示动态行程建议。</p>
    <template v-else>
      <p class="summary">{{ result.summary }}</p>
      <h3>行程建议</h3>
      <ul>
        <li v-for="(item, idx) in result.itinerary" :key="idx">
          D{{ item.day }} {{ item.period }} - {{ item.activity }}（{{ item.reason }}）
        </li>
      </ul>
      <h3>文化建议</h3>
      <ul>
        <li v-for="(tip, idx) in result.culture_tips" :key="`c-${idx}`">{{ tip }}</li>
      </ul>
      <h3>避坑提示</h3>
      <ul>
        <li v-for="(alert, idx) in result.risk_alerts" :key="`r-${idx}`">{{ alert }}</li>
      </ul>
      <h3>依据信号</h3>
      <ul>
        <li v-for="(basis, idx) in result.signal_basis" :key="`s-${idx}`">{{ basis }}</li>
      </ul>
    </template>
  </section>
</template>

<script setup lang="ts">
import type { PlanResult } from "../api/planner";

defineProps<{
  result: PlanResult | null;
  loading: boolean;
  error: string;
  stage: "idle" | "loading" | "partial" | "final" | "error";
}>();
</script>
