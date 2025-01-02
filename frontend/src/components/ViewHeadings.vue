<script>
export default {
  name: "ViewHeadings",
  props: {
    ViewHeading: {
      type: String,
      required: true
    },
  }
}
</script>

<template>
<div>
  <h1> {{ ViewHeading }} </h1>
</div>
</template>

<style scoped>

</style>