<template>
  <layout-ui>
    <template v-slot:main>
      <div class="row">
        <DashboardHeading title="Update Ad Request"></DashboardHeading>
      </div>
      <div class="form-container">
        <div class="row">
          <div class="col-md-6 content">
            <form>
              <div class="form-group">
                <label for="campaign_id">Campaign ID</label>
                <input type="number" class="form-control shadow-none" id="campaign_id" v-model="ad.campaign_id"
                       required>
              </div>
              <div class="form-group">
                <label for="influencer_id">Influencer ID</label>
                <input type="number" class="form-control shadow-none" id="influencer_id" v-model="ad.influencer_id"
                       required>
              </div>
              <div class="form-group">
                <label for="requirements">Requirements</label>
                <textarea class="form-control shadow-none" id="requirements" v-model="ad.requirements"></textarea>
              </div>
            </form>
          </div>
          <div class="col-md-6 content">
            <div class="form-group">
              <label for="status">Status</label>
              <select class="form-control shadow-none" id="status" v-model="ad.status" required>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="declined">Declined</option>
                <option value="completed">Completed</option>
                <option value="negotiation">Negotiation</option>
              </select>
            </div>
            <div class="form-group">
              <label for="payment_amount">Payment Amount</label>
              <input type="number" class="form-control shadow-none" id="payment_amount" v-model="ad.payment_amount"
                     required>
            </div>
            <div class="button-container">
              <button type="submit" @click="updateAd" class="submit-btn text-center">Update Request</button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>
</template>

<script>
import DashboardHeading from "@/components/DashboardHeading.vue";
import LayoutUi from "@/components/LayoutUi.vue";

export default {
  name: "CreateAd",
  components: {LayoutUi, DashboardHeading},
  data() {
    return {}
  },
  computed: {
    adId() {
      return this.$route.params.id;
    },
    ad() {
      return this.$store.getters.getAd;
    },
    success(){
      return this.$store.getters.getStatus.success
    }
  },
  methods: {
    updateAd() {
      this.$store.dispatch("updateAd", this.ad);
      if (this.success) {
        this.$router.push(`/sponsor/ads-list/${this.ad.campaign_id}`);
        this.$store.commit("setSuccess", false);
      }
    }
  },
  async beforeMount() {
    await this.$store.dispatch("fetchAd", this.adId);
  },

};
</script>

<style scoped>
.form-container {
  padding: 1rem;
  border: 1px solid #E0E0E0;
  border-radius: 5px;
  margin: 1rem;
}


form .form-group {
  margin-top: 1em;
}


input, textarea, select {
  width: 30vw;
  padding: 0.5em;
  border-radius: 0.5em;
  border: 1px solid #39465B;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  box-shadow: none; /* Remove the default blue shadow */
  border-color: #39465B; /* Optional: Add your own border color */
}


.error {
  margin-bottom: -2rem;
  color: red;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}

.submit-btn {
  background-color: #506582;
  width: 30vw;
  color: white;
  padding: 8px;
  border-radius: 5px;
  font-size: 1.2rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
  margin-top: 2rem;
}

</style>