<template>
  <div class="already-link">
    <router-link :to="link"> {{ text }}</router-link>
  </div>
</template>

<script>
export default {
  props: ['text', 'link'],
  name: 'AlreadyLink',
}
</script>

<style scoped>


.already-link {
  color: #39465B;
  font-size: 1.2rem;
  font-weight: 600;
}


.already-link a {
  color: #39465B;
  text-decoration: none;
}
</style>