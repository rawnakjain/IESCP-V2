<script>
export default {
  name: "DashboardHeading",
  props: ['title']
}
</script>

<template>
  <div class="col-md-12 heading">
    <h1>{{title}}</h1>
  </div>
</template>

<style scoped>

.heading h1 {
  font-size: 2.5rem;
  font-weight: 400;
  color: #39465B;
  margin: 1.5rem 0 1rem 0;
}

.heading {
  border-bottom: 2px solid #E0E0E0;
}
</style>