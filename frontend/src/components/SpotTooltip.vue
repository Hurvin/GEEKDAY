<template>
  <span 
    class="spot-tooltip-wrapper"
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
  >
    <span class="spot-highlight">{{ name }}</span>
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="show" class="spot-popover" :style="popoverStyle">
          <img :src="imageUrl" :alt="name" class="spot-img" loading="lazy" />
          <div class="spot-name">{{ name }}</div>
        </div>
      </Transition>
    </Teleport>
  </span>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { spotImages } from "../data/spots";

const props = defineProps<{
  name: string;
}>();

const show = ref(false);
const popoverStyle = ref<Record<string, string>>({});

const imageUrl = computed(() => {
  return spotImages[props.name] || "";
});

function onMouseEnter(event: MouseEvent) {
  const target = event.currentTarget as HTMLElement;
  const rect = target.getBoundingClientRect();
  
  popoverStyle.value = {
    top: `${rect.top - 10}px`,
    left: `${rect.left + rect.width / 2}px`,
  };
  show.value = true;
}

function onMouseLeave() {
  show.value = false;
}
</script>

<style scoped>
.spot-tooltip-wrapper {
  position: relative;
  display: inline; /* Changed to inline for better text flow */
  cursor: help;
}

.spot-highlight {
  color: #4ef5d6; /* Hardcoded accent color for now to match theme */
  font-weight: 500;
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 4px;
  transition: all 0.2s ease;
}

.spot-highlight:hover {
  background: rgba(78, 245, 214, 0.1);
  border-radius: 4px;
}

.spot-popover {
  position: fixed; /* Changed to fixed for Teleport */
  transform: translateX(-50%) translateY(-100%); /* Center horizontally and move above */
  width: 240px;
  background: rgba(20, 20, 25, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
  z-index: 9999; /* High z-index */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  pointer-events: none;
}

/* Arrow logic is harder with fixed position, skipping for now or can add a separate element */

.spot-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
}

.spot-name {
  margin-top: 8px;
  text-align: center;
  font-size: 14px;
  color: #f0f3ff;
  font-weight: 500;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(calc(-100% + 10px));
}
</style>
