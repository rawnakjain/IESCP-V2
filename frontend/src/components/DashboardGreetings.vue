<template>
  <h1>{{ greeting }}, {{ username }} </h1>
</template>

<script>
export default {
  name: "DashboardGreetings",
  props: ['greeting'],
  computed: {
  username() {
    return JSON.parse(localStorage.getItem("username"));
  }
}
}
</script>

<style scoped>

h1 {
  font-size: 2.5rem;
  font-weight: 400;
  color: #39465B;
  margin: 1.5rem 0 1rem 0;
}
</style>