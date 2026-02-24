<template>
  <section class="glass-card result">
    <h2>Agent 输出</h2>
    <p v-if="loading && stage === 'loading'">正在接收需求并启动动态规划...</p>
    <p v-else-if="loading && stage === 'partial'">已获取部分信号，正在整合文化规则与避坑策略...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!result">提交需求后将展示动态行程建议。</p>
    <template v-else>
      <p class="summary">{{ result.summary }}</p>
      
      <!-- New: Social Events Section -->
      <div v-if="result.social_events && result.social_events.length > 0" class="social-events-box">
        <h3>✨ 本地限时活动 (社交媒体雷达)</h3>
        <div class="event-grid">
          <div v-for="(event, idx) in result.social_events" :key="`ev-${idx}`" class="event-card">
            <div class="event-header">
              <span class="event-type">{{ event.type }}</span>
              <span class="event-source">{{ event.source }}</span>
            </div>
            <h4>{{ event.title }}</h4>
            <p class="event-time">🕒 {{ event.time_desc }}</p>
            <p class="event-loc">📍 {{ event.location }}</p>
            <p class="event-desc">{{ event.desc }}</p>
          </div>
        </div>
      </div>

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

<style scoped>
.social-events-box {
  margin: 20px 0;
  padding: 16px;
  background: rgba(35, 143, 137, 0.1);
  border: 1px solid rgba(78, 245, 214, 0.3);
  border-radius: 8px;
}

.social-events-box h3 {
  margin-top: 0;
  color: var(--accent);
  font-size: 1.1rem;
}

.event-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.event-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.event-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.8rem;
}

.event-type {
  background: rgba(110, 141, 255, 0.2);
  color: #c3cbf4;
  padding: 2px 6px;
  border-radius: 4px;
}

.event-source {
  color: var(--text-sub);
  font-style: italic;
}

.event-card h4 {
  margin: 0 0 6px;
  font-size: 1rem;
  color: #f0f3ff;
}

.event-time, .event-loc {
  margin: 2px 0;
  font-size: 0.85rem;
  color: #b7f9eb;
}

.event-desc {
  margin-top: 8px;
  font-size: 0.9rem;
  color: var(--text-sub);
  line-height: 1.5;
}
</style>
