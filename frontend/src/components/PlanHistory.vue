<template>
  <div class="glass-card history-panel">
    <h3>历史行程</h3>
    <div v-if="plans.length === 0" class="empty-state">暂无历史记录</div>
    <ul v-else class="history-list">
      <li 
        v-for="plan in plans" 
        :key="plan.id" 
        class="history-item" 
        :class="{ active: activeId === plan.id }"
        @click="$emit('select', plan)"
      >
        <div class="history-info">
          <span class="history-dest">{{ plan.payload.destination }} {{ plan.payload.days }}日游</span>
          <span class="history-date">{{ formatDate(plan.timestamp) }}</span>
        </div>
        <button class="delete-btn" @click.stop="$emit('delete', plan.id)" title="删除记录">×</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { SavedPlan } from "../api/planner";

defineProps<{
  plans: SavedPlan[];
  activeId?: string;
}>();

defineEmits<{
  (e: "select", plan: SavedPlan): void;
  (e: "delete", id: string): void;
}>();

function formatDate(ts: number) {
  return new Date(ts).toLocaleString("zh-CN", {
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });
}
</script>

<style scoped>
.history-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px; /* Limit height if list gets long */
  overflow: hidden;
}

h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #b7f9eb;
}

.empty-state {
  color: var(--text-sub);
  font-size: 0.9rem;
  padding: 12px 0;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(110, 141, 255, 0.15);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 245, 214, 0.3);
}

.history-item.active {
  background: rgba(78, 245, 214, 0.1);
  border-color: rgba(78, 245, 214, 0.6);
}

.history-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-dest {
  color: var(--text-main);
  font-weight: 500;
  font-size: 0.95rem;
}

.history-date {
  color: var(--text-sub);
  font-size: 0.8rem;
}

.delete-btn {
  background: transparent;
  border: none;
  color: var(--text-sub);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  opacity: 0.6;
  transition: all 0.2s;
}

.delete-btn:hover {
  opacity: 1;
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
}
</style>
