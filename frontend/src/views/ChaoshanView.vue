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
        </div>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
const spots = [
  {
    title: "汕头小公园开埠区",
    desc: "骑楼街区与老城烟火并存，适合夜游和拍照，能感受潮汕商业文化的历史脉络。",
    image:
      "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80",
  },
  {
    title: "潮州古城与牌坊街",
    desc: "古城墙、广济桥与牌坊街串联起潮州千年文脉，推荐慢节奏步行体验。",
    image:
      "https://images.unsplash.com/photo-1530789253388-582c481c54b0?auto=format&fit=crop&w=1200&q=80",
  },
  {
    title: "英歌舞与工夫茶文化",
    desc: "一动一静代表潮汕精神：英歌舞热烈奔放，工夫茶讲究礼序与慢生活。",
    image:
      "https://images.unsplash.com/photo-1482349212652-a7c2f54d0d2b?auto=format&fit=crop&w=1200&q=80",
  },
];
</script>
