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
    image:"/tp/8.jpg",
  },
  {
    title: "青澳湾",
    desc: "东方夏威夷，沙质细腻，是观赏日出的绝佳位置。",
    image:"/tp/9.jpg",
  },
];
</script>
