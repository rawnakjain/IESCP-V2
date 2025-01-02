<template>
  <layout-ui>
    <template v-slot:main>
      <div class="row">
        <DashboardHeading title="Create Ad"></DashboardHeading>
      </div>
      <div class="form-container">
        <div class="row">
          <div class="col-md-6 content">
            <form>
              <div class="form-group">
                <label for="campaign_id">Campaign ID</label>
                <input type="number" class="form-control shadow-none" id="campaign_id" v-model="form.campaign_id"
                       required>
              </div>
              <div class="form-group">
                <label for="influencer_id">Influencer ID</label>
                <input type="number" class="form-control shadow-none" id="influencer_id" v-model="form.influencer_id"
                       required>
              </div>
              <div class="form-group">
                <label for="requirements">Requirements</label>
                <textarea class="form-control shadow-none" id="requirements" v-model="form.requirements"></textarea>
              </div>
            </form>
          </div>
          <div class="col-md-6 content">
            <div class="form-group">
              <label for="payment_amount">Payment Amount</label>
              <input type="number" class="form-control shadow-none" id="payment_amount" v-model="form.payment_amount"
                     required>
            </div>

            <div class="button-container">
              <button type="submit" @click="createAd" class="submit-btn text-center">Create Request</button>
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
    return {
      form: {
        campaign_id: null,
        influencer_id: null,
        requirements: "",
        payment_amount: null,
        negotiated_payment_amount: null,
        status: "pending",
        madeby: JSON.stringify(localStorage.getItem("role")),
      }
    };
  },
  computed: {
    success() {
      return this.$store.getters.getStatus.success;
    },
  },
  methods: {
    createAd() {
      this.$store.dispatch("createAd", this.form);
      if (this.success) {
        this.$router.push("/sponsor/campaigns");
        this.$store.commit("setSuccess", false);
      }
    }
  },
   created() {
    this.form.madeby = this.role; // Set the value in the created hook
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