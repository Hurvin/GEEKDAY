<template>
  <div class="page-shell">
    <section class="hero section-card">
      <p class="section-tag">PLANNER</p>
      <p class="kicker">23.5°N CHAOSHAN INTEL TRIP AGENT</p>
      <h1>行程规划</h1>
      <p class="sub-title">输入约束与偏好，生成动态行程、文化建议和避坑提示。</p>
    </section>

    <section class="panel-grid" :class="{ 'has-result': stage !== 'idle' }">
      <div class="left-col">
        <PlannerForm :loading="loading" @submit="onSubmit" />
        <PlanHistory 
          v-if="history.length > 0"
          :plans="history" 
          :active-id="activePlanId" 
          @select="selectPlan" 
          @delete="deletePlan" 
        />
      </div>
      <ResultPanel 
        v-if="stage !== 'idle'"
        :result="result" 
        :loading="loading" 
        :error="error" 
        :stage="stage" 
      />
    </section>

    <!-- Weather Alert Modal -->
    <div v-if="weatherAlert.show" class="weather-modal-mask">
      <div class="weather-modal">
        <h3>⚠️ 天气变化提醒</h3>
        <p class="weather-desc">
          监测到 <strong>{{ weatherAlert.destination }}</strong> 
          第 {{ weatherAlert.dayIndex }} 天天气发生变化：<br/>
          从「{{ weatherAlert.oldCondition }}」变为「<span class="highlight">{{ weatherAlert.newCondition }}</span>」
        </p>
        <p class="weather-hint">建议根据新天气调整行程安排。</p>
        <div class="weather-actions">
          <button class="neon-btn secondary" @click="ignoreWeatherChange">暂不调整</button>
          <button class="neon-btn" @click="regeneratePlan">重新生成行程</button>
        </div>
      </div>
    </div>

    <div v-if="crowdAlert.show" class="weather-modal-mask">
      <div class="weather-modal">
        <h3>⚠️ 人流量变化提醒</h3>
        <p class="weather-desc">
          监测到 <strong>{{ crowdAlert.destination }}</strong>
          第 {{ crowdAlert.dayIndex }} 天人流量发生变化：<br/>
          从「{{ crowdAlert.oldLevel }}」变为「<span class="highlight">{{ crowdAlert.newLevel }}</span>」
        </p>
        <p class="weather-hint">建议避开高峰时段或调整热门景点顺序。</p>
        <div class="weather-actions">
          <button class="neon-btn" @click="closeCrowdAlert">知道了</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-modal" role="status" aria-live="polite" aria-label="模型回复中">
      <div class="loading-modal-content">
        <img src="/jz.gif" alt="模型思考中" class="loading-modal-gif" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, reactive } from "vue";

import PlannerForm from "../components/PlannerForm.vue";
import ResultPanel from "../components/ResultPanel.vue";
import PlanHistory from "../components/PlanHistory.vue";
import {
  createPlan,
  fetchFakeEvents,
  fetchWeather,
  type FakeSignalEvent,
  type PlanPayload,
  type PlanResult,
  type SavedPlan,
} from "../api/planner";

const loading = ref(false);
const error = ref("");
const result = ref<PlanResult | null>(null);
const stage = ref<"idle" | "loading" | "partial" | "final" | "error">("idle");
const history = ref<SavedPlan[]>([]);
const activePlanId = ref<string | undefined>(undefined);

// Weather Monitoring State
const weatherAlert = reactive({
  show: false,
  destination: "",
  dayIndex: 1,
  oldCondition: "",
  newCondition: "",
});
const crowdAlert = reactive({
  show: false,
  destination: "",
  dayIndex: 1,
  oldLevel: "",
  newLevel: "",
});

const pendingFakeEvents = ref<FakeSignalEvent[]>([]);
const lastWeatherCondition = ref("");
let weatherTimer: number | undefined;
let fakeEventTimer: number | undefined;

onMounted(() => {
  const saved = localStorage.getItem("chaoyun_plans");
  if (saved) {
    try {
      history.value = JSON.parse(saved);
    } catch {
      history.value = [];
    }
  }
  
  // Check test mode
  const isTestMode = localStorage.getItem("chaoyun_test_mode") === "true";
  
  // Start polling
  // Normal mode: 10 minutes (600,000 ms)
  // Test mode: 60 seconds (60,000 ms) - to ensure we catch the minute change
  const interval = isTestMode ? 60000 : 600000;
  weatherTimer = setInterval(checkWeather, interval);

  // Fake signal events are used for rapid manual demo/testing.
  fakeEventTimer = setInterval(consumeFakeEvents, 3000);
  consumeFakeEvents();
});

onUnmounted(() => {
  if (weatherTimer) clearInterval(weatherTimer);
  if (fakeEventTimer) clearInterval(fakeEventTimer);
});

function showNextFakeEvent() {
  if (weatherAlert.show || crowdAlert.show || pendingFakeEvents.value.length === 0) {
    return;
  }

  const evt = pendingFakeEvents.value.shift();
  if (!evt) return;

  if (evt.event_type === "weather") {
    weatherAlert.destination = evt.destination || "当前目的地";
    weatherAlert.dayIndex = evt.day_index || 1;
    weatherAlert.oldCondition = evt.old_value || "未知";
    weatherAlert.newCondition = evt.new_value || "未知";
    weatherAlert.show = true;
    return;
  }

  crowdAlert.destination = evt.destination || "当前目的地";
  crowdAlert.dayIndex = evt.day_index || 1;
  crowdAlert.oldLevel = evt.old_value || "未知";
  crowdAlert.newLevel = evt.new_value || "未知";
  crowdAlert.show = true;
}

async function consumeFakeEvents() {
  try {
    const resp = await fetchFakeEvents();
    if (resp.events.length === 0) return;
    pendingFakeEvents.value.push(...resp.events);
    showNextFakeEvent();
  } catch {
    // Keep silent to avoid interrupting normal planner flow.
  }
}

async function checkWeather() {
  // Only check if we have an active plan/result
  if (!result.value || !activePlanId.value) return;
  
  // Find current plan payload to get destination
  const currentPlan = history.value.find(p => p.id === activePlanId.value);
  if (!currentPlan) return;
  
  const dest = currentPlan.payload.destination;
  const days = currentPlan.payload.days || 1;
  
  try {
    const weatherData = await fetchWeather(dest, days);
    // Assuming weatherData returns { forecast: [{day: 1, condition: "..."}] }
    const currentForecast = weatherData.forecast || [];
    
    // Parse baseline
    let baseline = [];
    try {
      baseline = JSON.parse(lastWeatherCondition.value || "[]");
    } catch {
      baseline = [];
    }
    
    // If we haven't stored initial weather yet, just store it
    if (baseline.length === 0) {
      lastWeatherCondition.value = JSON.stringify(currentForecast);
      return;
    }
    
    // Compare each day
    let changedDay = null;
    let oldVal = "";
    let newVal = "";
    
    for (let i = 0; i < currentForecast.length; i++) {
      const dayNew = currentForecast[i];
      const dayOld = baseline.find((d: any) => d.day === dayNew.day);
      
      if (dayOld && dayOld.condition !== dayNew.condition) {
        changedDay = dayNew.day;
        oldVal = dayOld.condition;
        newVal = dayNew.condition;
        break; // Alert on first change found
      }
    }
    
    if (changedDay !== null) {
      weatherAlert.destination = dest;
      weatherAlert.dayIndex = changedDay;
      weatherAlert.oldCondition = oldVal;
      weatherAlert.newCondition = newVal;
      weatherAlert.show = true;
      
      // Update last known condition to current full forecast so we don't alert again for same change
      lastWeatherCondition.value = JSON.stringify(currentForecast);
    }
  } catch (e) {
    console.error("Weather check failed", e);
  }
}

function ignoreWeatherChange() {
  weatherAlert.show = false;
  showNextFakeEvent();
}

function closeCrowdAlert() {
  crowdAlert.show = false;
  showNextFakeEvent();
}

function regeneratePlan() {
  weatherAlert.show = false;
  const currentPlan = history.value.find(p => p.id === activePlanId.value);
  if (currentPlan) {
    // Re-submit the same payload
    onSubmit(currentPlan.payload);
  }
}

function savePlan(payload: PlanPayload, res: PlanResult) {
  const newPlan: SavedPlan = {
    id: Date.now().toString(),
    timestamp: Date.now(),
    payload,
    result: res,
  };
  history.value.unshift(newPlan);
  localStorage.setItem("chaoyun_plans", JSON.stringify(history.value));
  activePlanId.value = newPlan.id;
  
  // Initialize weather baseline for the new plan
  // We should ideally fetch it now or extract from plan result if available
  // For now, we'll let the next poll or immediate check handle it
  // Let's do an immediate check to set baseline without alerting
  updateWeatherBaseline(payload.destination, payload.days);
}

async function updateWeatherBaseline(city: string, days: number = 1) {
  try {
    const data = await fetchWeather(city, days);
    lastWeatherCondition.value = JSON.stringify(data.forecast || []);
  } catch {
    lastWeatherCondition.value = "";
  }
}

function selectPlan(plan: SavedPlan) {
  result.value = plan.result;
  activePlanId.value = plan.id;
  stage.value = "final";
  window.scrollTo({ top: 0, behavior: "smooth" });
  
  // Reset weather baseline for selected plan
  updateWeatherBaseline(plan.payload.destination, plan.payload.days);
}

function deletePlan(id: string) {
  if (!confirm("确定要删除这条记录吗？")) return;
  history.value = history.value.filter((p) => p.id !== id);
  localStorage.setItem("chaoyun_plans", JSON.stringify(history.value));
  if (activePlanId.value === id) {
    activePlanId.value = undefined;
    result.value = null;
    stage.value = "idle";
    lastWeatherCondition.value = "";
  }
}

async function onSubmit(payload: PlanPayload) {
  loading.value = true;
  error.value = "";
  stage.value = "loading";
  activePlanId.value = undefined;
  
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
    const res = await createPlan({
      ...payload,
      model: selectedModel || undefined,
    });
    result.value = res;
    stage.value = "final";
    savePlan(payload, res);
  } catch (err) {
    error.value = err instanceof Error ? err.message : "请求失败，请重试";
    stage.value = "error";
  } finally {
    clearTimeout(partialTimer);
    loading.value = false;
  }
}
</script>

<style scoped>
.panel-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
  transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.panel-grid.has-result {
  grid-template-columns: 350px 1fr;
  max-width: 1400px;
}

.left-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.weather-modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.loading-modal {
  position: fixed;
  inset: 0;
  z-index: 1500;
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

.weather-modal {
  background: linear-gradient(160deg, rgba(26, 18, 68, 0.95), rgba(20, 14, 52, 0.98));
  border: 1px solid rgba(78, 245, 214, 0.4);
  box-shadow: 0 0 40px rgba(78, 245, 214, 0.15);
  border-radius: 16px;
  padding: 24px;
  width: min(400px, 90vw);
  text-align: center;
  animation: slide-up 0.3s ease-out;
}

.weather-modal h3 {
  margin: 0 0 16px;
  color: #ffda79;
  font-size: 1.25rem;
}

.weather-desc {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-main);
  margin-bottom: 12px;
}

.highlight {
  color: var(--accent);
  font-weight: bold;
}

.weather-hint {
  color: var(--text-sub);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.weather-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.neon-btn.secondary {
  background: transparent;
  border-color: rgba(141, 161, 255, 0.4);
  color: var(--text-sub);
}

.neon-btn.secondary:hover {
  border-color: rgba(141, 161, 255, 0.8);
  color: var(--text-main);
  box-shadow: none;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
