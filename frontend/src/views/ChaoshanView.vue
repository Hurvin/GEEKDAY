<template>
  <div class="page-shell">
    <section class="section-card">
      <p class="section-tag">CHAOSHAN</p>
      <h1>走进潮汕</h1>
      <p class="sub-title">从地标建筑、非遗文化到在地美食，快速了解潮汕旅行的魅力。</p>
    </section>

    <section class="spot-grid">
      <article v-for="spot in spots" :key="spot.title" class="spot-card">
        <img class="spot-image" :src="spot.image" :alt="spot.title" loading="lazy" />
        <div class="spot-content">
          <h3>{{ spot.title }}</h3>
          <p>{{ spot.desc }}</p>
          <button class="comment-btn" @click="openCommentModal(spot.title)">
            📝 写评论
          </button>
        </div>
      </article>
    </section>

    <!-- 评论弹窗 -->
    <div v-if="showModal" class="modal-mask" @click.self="closeModal">
      <div class="modal-content glass-card">
        <h3>评价：{{ currentSpot }}</h3>
        
        <div class="comments-list">
          <div v-if="getComments(currentSpot).length === 0" class="empty-comment">
            暂无评论，快来抢沙发！
          </div>
          <div v-else v-for="(c, idx) in getComments(currentSpot)" :key="idx" class="comment-item">
            <div class="comment-header">
              <span class="user-name">游客{{ c.userId.slice(-4) }}</span>
              <span class="comment-time">{{ new Date(c.timestamp).toLocaleDateString() }}</span>
            </div>
            <p class="comment-text">{{ c.text }}</p>
          </div>
        </div>

        <form @submit.prevent="submitComment" class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="分享你的游玩体验..." 
            rows="3"
            required
          ></textarea>
          <button type="submit" class="neon-btn small">发布</button>
        </form>
        
        <button class="close-btn" @click="closeModal">×</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";

const spots = [
  {
    title: "汕头小公园开埠区",
    desc: "骑楼街区与老城烟火并存，适合夜游和拍照，能感受潮汕商业文化的历史脉络。",
    image: "/tp/6.jpg",
  },
  {
    title: "潮州古城与牌坊街",
    desc: "古城墙、广济桥与牌坊街串联起潮州千年文脉，推荐慢节奏步行体验。",
    image:"/tp/5.jpg",
  },
  {
    title: "潮州龙湖古寨",
    desc: "这里充满了松弛感，一半是生活，一半是历史，仿佛时间都慢了下来",
    image: "/tp/1.jpg",
  },
  {
    title: "潮州西湖",
    desc: "满屏的绿意以及蓬勃的树张力，沐浴在湖畔氧吧中，攒足探索的生命力",
    image: "/tp/2.jpg",
  },
  {
    title: "青龙古庙",
    desc: "庙顶嵌瓷堪称一绝，不愧被称为屋顶上的艺术",
    image: "/tp/3.jpg",
  },
  {
    title: "古城街巷",
    desc: "可以在义安路,西马路与甲第巷等街巷多走走，逛吃逛喝的同时感受潮州烟火",
    image: "/tp/4.jpg",
  },
  {
    title: "英歌舞与工夫茶文化",
    desc: "一动一静代表潮汕精神：英歌舞热烈奔放，工夫茶讲究礼序与慢生活。",
    image:"/tp/7.jpg",
  },
  {
    title: "南澳岛",
    desc: "北回归线上的绿洲，拥有绝美的环岛公路和灯塔。",
    image: "/tp/8.jpg",
  },
  {
    title: "青澳湾",
    desc: "东方夏威夷，沙质细腻，是观赏日出的绝佳位置。",
    image: "/tp/9.jpg",
  },
];

// Comment System Logic
interface Comment {
  spotName: string;
  userId: string;
  text: string;
  timestamp: number;
}

const showModal = ref(false);
const currentSpot = ref("");
const newComment = ref("");
const allComments = ref<Comment[]>([]);

onMounted(() => {
  const saved = localStorage.getItem("chaoyun_spot_comments");
  if (saved) {
    try {
      allComments.value = JSON.parse(saved);
    } catch {
      allComments.value = [];
    }
  }
});

function openCommentModal(spotName: string) {
  currentSpot.value = spotName;
  showModal.value = true;
  newComment.value = "";
}

function closeModal() {
  showModal.value = false;
}

function getComments(spotName: string) {
  return allComments.value
    .filter(c => c.spotName === spotName)
    .sort((a, b) => b.timestamp - a.timestamp);
}

function submitComment() {
  if (!newComment.value.trim()) return;
  
  const comment: Comment = {
    spotName: currentSpot.value,
    userId: Date.now().toString(), // Simple mock ID
    text: newComment.value,
    timestamp: Date.now(),
  };
  
  allComments.value.push(comment);
  localStorage.setItem("chaoyun_spot_comments", JSON.stringify(allComments.value));
  newComment.value = "";
}
</script>

<style scoped>
.comment-btn {
  margin-top: 12px;
  background: rgba(78, 245, 214, 0.1);
  border: 1px solid rgba(78, 245, 214, 0.3);
  color: var(--accent);
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.comment-btn:hover {
  background: rgba(78, 245, 214, 0.2);
  transform: translateY(-1px);
}

/* Modal Styles */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  width: 90%;
  max-width: 500px;
  padding: 24px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 80vh;
}

.modal-content h3 {
  margin: 0;
  color: var(--text-main);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 12px;
}

.comments-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 150px;
}

.empty-comment {
  text-align: center;
  color: var(--text-sub);
  padding: 20px 0;
  font-style: italic;
}

.comment-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 6px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 0.8rem;
}

.user-name {
  color: var(--accent);
  font-weight: 500;
}

.comment-time {
  color: var(--text-sub);
}

.comment-text {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #eee;
  margin: 0;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

textarea {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(110, 141, 255, 0.2);
  border-radius: 6px;
  padding: 10px;
  color: var(--text-main);
  resize: vertical;
}

textarea:focus {
  border-color: var(--accent);
  outline: none;
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: none;
  color: var(--text-sub);
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: #fff;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
