<template>
  <div class="page-shell">
    <section class="section-card">
      <p class="section-tag">PROFILE</p>
      <h1>我的旅行信息</h1>
      <p class="sub-title">设置你的基础信息和偏好，帮助 Agent 给出更贴合你的行程。</p>
    </section>

    <form class="glass-card form" @submit.prevent="saveProfile">
      <!-- 基础信息 -->
      <div class="form-section">
        <h3>基础信息</h3>
        <div class="grid-2">
          <label>
            您的姓名/昵称
            <input v-model="profile.name" placeholder="例如：Light" />
          </label>
          <label>
            出发城市
            <input v-model="profile.departureCity" placeholder="例如：广州" />
          </label>
        </div>
        <div class="grid-2">
          <label>
            常住城市
            <input v-model="profile.homeCity" placeholder="例如：深圳" />
          </label>
          <label>
            预算偏好
            <select v-model="profile.budgetLevel">
              <option value="经济">经济型 (注重性价比)</option>
              <option value="中等">舒适型 (均衡体验)</option>
              <option value="品质">豪华型 (享受服务)</option>
            </select>
          </label>
        </div>
      </div>

      <!-- 衣食住行偏好 -->
      <div class="form-section">
        <h3>衣食住行偏好</h3>
        
        <div class="grid-2">
          <!-- 衣 -->
          <label>
            👗 穿搭风格 (衣)
            <select v-model="profile.clothingStyle">
              <option>休闲舒适 (以走路为主)</option>
              <option>出片穿搭 (适合拍照)</option>
              <option>汉服/国风 (古城适配)</option>
              <option>清凉海岛 (南澳适配)</option>
            </select>
          </label>

          <!-- 住 -->
          <label>
            🏨 住宿类型 (住)
            <select v-model="profile.accommodationType">
              <option>经济型酒店 (性价比)</option>
              <option>特色民宿 (体验当地风情)</option>
              <option>高档酒店 (舒适服务)</option>
              <option>青旅 (结交朋友)</option>
            </select>
          </label>
        </div>

        <div class="grid-2">
          <!-- 行 -->
          <label>
            🚗 交通方式 (行)
            <select v-model="profile.transportPreference">
              <option>网约车/出租车</option>
              <option>自驾/租车</option>
              <option>公交/共享电单车</option>
              <option>包车游</option>
            </select>
          </label>
          <div></div>
        </div>

        <!-- 食 -->
        <label>
          🍜 饮食偏好 (食 - 多选)
          <div class="checkbox-group">
            <label v-for="opt in foodOptions" :key="opt">
              <input type="checkbox" :value="opt" v-model="profile.foodPreferences">
              {{ opt }}
            </label>
          </div>
        </label>
      </div>

      <!-- 补充信息 -->
      <div class="form-section">
        <h3>同行人员档案</h3>
        <p class="section-desc">为你的家人和朋友建立档案，生成独立的用户配置文件，让 Agent 为每个人量身定制。</p>
        
        <div class="companions-list" v-if="profile.companions && profile.companions.length > 0">
          <div v-for="(person, idx) in profile.companions" :key="idx" class="companion-card">
            <div class="companion-header">
              <span class="companion-name">{{ person.name }}</span>
              <span class="companion-tag">{{ person.relation }}</span>
              <button class="delete-btn" type="button" @click="removeCompanion(idx)">×</button>
            </div>
            <div class="companion-details">
              <span>{{ person.ageGroup }}</span>
              <span v-if="person.healthCondition" :title="person.healthCondition">🩺</span>
            </div>
            <div class="companion-pref">
               <span v-if="person.preferences && person.preferences.length > 0">
                 ❤️ {{ person.preferences.join('、') }}
               </span>
               <span v-else class="text-sub">暂无偏好</span>
            </div>
            <button class="neon-btn secondary small-btn edit-btn" type="button" @click="editCompanion(idx)">
              编辑档案
            </button>
          </div>
        </div>

        <div class="add-companion-box glass-card-inner">
          <h4>{{ isEditingCompanion ? '编辑档案' : '新建档案' }}</h4>
          
          <div class="grid-2">
            <label>
              姓名/称呼
              <input v-model="currentCompanion.name" placeholder="例如：爸爸" />
            </label>
            <label>
              关系
              <select v-model="currentCompanion.relation">
                <option value="" disabled>选择关系</option>
                <option>朋友</option>
                <option>伴侣</option>
                <option>父母</option>
                <option>子女</option>
                <option>亲戚</option>
                <option>其他</option>
              </select>
            </label>
          </div>
          
          <div class="grid-2">
            <label>
              年龄段
              <select v-model="currentCompanion.ageGroup">
                <option value="" disabled>选择年龄段</option>
                <option>儿童 (0-12)</option>
                <option>青少年 (13-18)</option>
                <option>青年 (19-35)</option>
                <option>中年 (36-60)</option>
                <option>老年 (60+)</option>
              </select>
            </label>
            <label>
              健康/特殊情况
              <input v-model="currentCompanion.healthCondition" placeholder="如：腿脚不便、过敏" />
            </label>
          </div>

          <label>
             个人偏好 (兴趣/忌口等)
             <input v-model="currentCompanion.prefInput" placeholder="输入偏好，用空格分隔" />
          </label>

          <div class="action-row">
            <button v-if="isEditingCompanion" class="neon-btn secondary" type="button" @click="cancelEditCompanion">取消</button>
            <button class="neon-btn" type="button" @click="saveCompanion" :disabled="!currentCompanion.name || !currentCompanion.relation">
              {{ isEditingCompanion ? '保存修改' : '+ 添加档案' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 补充信息 -->
      <div class="form-section">
        <h3>补充说明</h3>
        <label>
          其他备注
          <textarea v-model="profile.note" rows="3" placeholder="例如：对海鲜过敏、携带宠物等..."></textarea>
        </label>
      </div>

      <button class="neon-btn submit-btn" type="submit">保存我的信息</button>
      <p v-if="saved" class="save-toast">✨ 信息已更新，Agent 将记住你的偏好！</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";

const foodOptions = ["牛肉火锅", "生腌", "卤鹅", "肠粉/粿条", "功夫茶", "甜汤", "深夜大排档"];

type Companion = {
  name: string;
  relation: string;
  ageGroup?: string;
  healthCondition?: string;
  preferences?: string[];
};

type ProfileData = {
  name: string;
  departureCity: string;
  homeCity: string;
  budgetLevel: string;
  clothingStyle: string;
  foodPreferences: string[];
  accommodationType: string;
  transportPreference: string;
  note: string;
  companions: Companion[];
};

const profile = reactive<ProfileData>({
  name: "",
  departureCity: "",
  homeCity: "",
  budgetLevel: "中等",
  clothingStyle: "休闲舒适 (以走路为主)",
  foodPreferences: [],
  accommodationType: "经济型酒店 (性价比)",
  transportPreference: "网约车/出租车",
  note: "",
  companions: [],
});

const isEditingCompanion = ref(false);
const editingIndex = ref(-1);

const currentCompanion = reactive({
  name: "",
  relation: "",
  ageGroup: "",
  healthCondition: "",
  prefInput: "",
});

const saved = ref(false);

function resetCompanionForm() {
  currentCompanion.name = "";
  currentCompanion.relation = "";
  currentCompanion.ageGroup = "";
  currentCompanion.healthCondition = "";
  currentCompanion.prefInput = "";
  isEditingCompanion.value = false;
  editingIndex.value = -1;
}

function saveCompanion() {
  if (!currentCompanion.name || !currentCompanion.relation) return;
  
  const prefs = currentCompanion.prefInput.split(/[\s,，、]+/).filter(Boolean);
  
  const companionData: Companion = {
    name: currentCompanion.name,
    relation: currentCompanion.relation,
    ageGroup: currentCompanion.ageGroup,
    healthCondition: currentCompanion.healthCondition,
    preferences: prefs,
  };

  if (isEditingCompanion.value && editingIndex.value >= 0) {
    profile.companions[editingIndex.value] = companionData;
  } else {
    profile.companions.push(companionData);
  }

  resetCompanionForm();
}

function editCompanion(idx: number) {
  const c = profile.companions[idx];
  currentCompanion.name = c.name;
  currentCompanion.relation = c.relation;
  currentCompanion.ageGroup = c.ageGroup || "";
  currentCompanion.healthCondition = c.healthCondition || "";
  currentCompanion.prefInput = (c.preferences || []).join(" ");
  
  isEditingCompanion.value = true;
  editingIndex.value = idx;
}

function cancelEditCompanion() {
  resetCompanionForm();
}

function removeCompanion(idx: number) {
  if (confirm("确定删除该档案吗？")) {
    profile.companions.splice(idx, 1);
    if (editingIndex.value === idx) {
      resetCompanionForm();
    }
  }
}

function saveProfile() {
  localStorage.setItem("chaoyun_profile", JSON.stringify(profile));
  saved.value = true;
  setTimeout(() => saved.value = false, 3000);
}

onMounted(() => {
  const cached = localStorage.getItem("chaoyun_profile");
  if (cached) {
    try {
      const parsed = JSON.parse(cached);
      profile.name = parsed.name ?? "";
      profile.departureCity = parsed.departureCity ?? "";
      profile.homeCity = parsed.homeCity ?? "";
      profile.budgetLevel = parsed.budgetLevel ?? "中等";
      profile.clothingStyle = parsed.clothingStyle ?? "休闲舒适 (以走路为主)";
      profile.foodPreferences = Array.isArray(parsed.foodPreferences) ? parsed.foodPreferences : [];
      profile.accommodationType = parsed.accommodationType ?? "经济型酒店 (性价比)";
      profile.transportPreference = parsed.transportPreference ?? "网约车/出租车";
      profile.note = parsed.note ?? "";
      profile.companions = Array.isArray(parsed.companions) ? parsed.companions : [];
    } catch (e) {
      console.error("Failed to parse profile", e);
    }
  }
});
</script>

<style scoped>
.page-shell {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px;
  margin-top: 24px;
}

h3 {
  font-size: 1.1rem;
  color: var(--accent);
  margin: 0 0 16px 0;
  border-left: 3px solid var(--accent);
  padding-left: 10px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.95rem;
  color: var(--text-sub);
}

input, select, textarea {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(110, 141, 255, 0.2);
  border-radius: 6px;
  padding: 10px 14px;
  color: var(--text-main);
  font-size: 1rem;
  transition: all 0.2s;
  width: 100%;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--accent);
  outline: none;
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 0 2px rgba(78, 245, 214, 0.1);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-group label {
  flex-direction: row;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.05);
  padding: 8px 14px;
  border-radius: 20px;
  border: 1px solid transparent;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.checkbox-group label:has(input:checked) {
  background: rgba(78, 245, 214, 0.15);
  border-color: rgba(78, 245, 214, 0.4);
  color: var(--accent);
  font-weight: 500;
}

.submit-btn {
  margin-top: 20px;
  width: 100%;
  justify-content: center;
  font-size: 1.1rem;
  padding: 14px;
}

.save-toast {
  text-align: center;
  color: #4ef5d6;
  font-size: 0.95rem;
  margin-top: 10px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
  
  .form {
    padding: 20px;
  }
}

.companions-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.companion-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(141, 161, 255, 0.2);
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.companion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.companion-name {
  font-weight: bold;
  color: var(--text-main);
}

.companion-tag {
  background: rgba(78, 245, 214, 0.15);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.delete-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 4px;
}

.companion-details {
  display: flex;
  gap: 8px;
  font-size: 0.85rem;
  color: var(--text-sub);
}

.add-companion-box {
  background: rgba(0, 0, 0, 0.2);
  padding: 16px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.companion-pref {
  font-size: 0.8rem;
  color: var(--text-main);
  background: rgba(0,0,0,0.2);
  padding: 4px 8px;
  border-radius: 4px;
}

.text-sub {
  color: var(--text-sub);
  font-style: italic;
}

.edit-btn {
  margin-top: auto;
  align-self: flex-start;
  padding: 4px 10px;
  font-size: 0.8rem;
}

.action-row {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 10px;
}

.section-desc {
  margin: -10px 0 16px;
  color: var(--text-sub);
  font-size: 0.9rem;
}
</style>
