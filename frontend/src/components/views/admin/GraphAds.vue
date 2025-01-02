<script>
import {Bar} from "vue-chartjs";

export default {
  name: "GraphAds",
  components: {Bar},
  data() {
    return {
      chartData: {
        labels: this.$store.getters.getAdsData['statuses'],
        datasets: [
          {
            data: this.$store.getters.getAdsData['ad_counts'],
            label: 'Ad Requests',
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
          }],
        borderWidth: 1,

      },
      chartOptions: {
        responsive: true,
      },
    }
  },

  beforeMount() {
    this.$store.dispatch('fetchAdsData')
  }
}
</script>

<template>
  <bar :data="chartData" :options="chartOptions"></bar>
</template>

<style scoped>

</style>