<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="My AdRequests"></DashboardHeading>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <p class="alert alert-secondary" role="alert" v-if="adStatus"> {{ adStatus }} </p>
            <div class="table-container table-responsive">
              <table>
                <thead>
                <tr>
                  <th scope="col">Id</th>
                  <th scope="col">Campaign Id</th>
                  <th scope="col">Requirements</th>
                  <th scope="col">Payment</th>
                  <th scope="col">Status</th>
                  <th scope="col">Made By</th>
                  <th scope="col">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="ad in ads" :key="ad.id">
                  <td>{{ ad.id }}</td>
                  <td>{{ ad.campaign_id }}</td>
                  <td>{{ ad.requirements }}</td>
                  <td>{{ ad.payment_amount }} <span
                      v-if="ad.negotiated_payment_amount"> > {{ ad.negotiated_payment_amount }} </span></td>
                  <td>{{ ad.status }}</td>
                  <td>{{ ad.madeby }}</td>
                  <td class="actions">
                    <i class="fa-solid fa-check"
                       v-if="((ad.madeby === 'sponsor') && (ad.status === 'pending'))|| ((ad.status === 'negotiation')&& (ad.negotiated_by === 'sponsor'))"
                       @click="approveAd(ad.id)"> </i>

                    <i class="fa-solid fa-xmark"
                       v-if="((ad.madeby === 'sponsor') && (ad.status === 'pending'))|| ((ad.status === 'negotiation')&& (ad.negotiated_by === 'sponsor'))"
                       @click="declineAd(ad.id)"> </i>
                    <button type="button"
                            v-if="((ad.madeby==='influencer') && (ad.status==='declined'))||(ad.madeby === 'sponsor') && (ad.status ==='pending')"
                            class="btn btn-view" data-bs-toggle="modal"
                            data-bs-target="#staticBackdrop" @click="setCurrentAdId(ad.id)">
                      Negotiate
                    </button>

                    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false"
                         tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                      <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h1 class="modal-title fs-5" id="staticBackdropLabel">What's Your Ask?</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <input type="number" v-model="negotiatedPaymentAmount"
                                   placeholder="Enter new payment amount" class="form-control">
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-view" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-view" @click="negotiateAd" data-bs-dismiss="modal">Ask
                              for New Price
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>


                    <button class="btn btn-view" v-if="ad.status === 'approved'">Waiting Completion</button>
                    <button class="btn btn-view" v-if="(ad.madeby !== role) && (ad.status ==='declined')">You Declined
                    </button>
                    <button class="btn btn-view" v-if="(ad.status ==='completed')">Completed</button>
                    <button class="btn btn-view"
                            v-if="((ad.madeby === role) && (ad.status ==='pending')) || ((ad.status==='negotiation') && (ad.negotiated_by === role))">
                      Wait
                    </button>
                  </td>
                </tr>
                </tbody>
              </table>
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
  name: "AdRequests",
  components: {LayoutUi, DashboardHeading},
  data() {
    return {
      negotiatedPaymentAmount: null,
      currentAdId: null,
    }
  },
  computed: {
    influencerUsername() {
      return JSON.parse(localStorage.getItem('username'));
    },
    ads() {
      return this.$store.getters.getInfluencerAds;
    },
    role() {
      return JSON.parse(localStorage.getItem('role'));
    },
    adStatus() {
      return this.$store.getters.getAdStatus;
    },
  },
  methods: {
    approveAd(adId) {
      this.$store.dispatch("approveAd", adId);
      if (this.success) {
        this.$store.commit("setSuccess", false);
        this.$router.push(`/sponsor/ads-list/${this.campaignId}`);
      }
    },
    declineAd(adId) {
      this.$store.dispatch("declineAd", adId);
    },
    setCurrentAdId(adId) {
      this.currentAdId = adId;
    },
    negotiateAd() {
      this.$store.dispatch("negotiateAd", {
        adId: this.currentAdId,
        negotiated_payment_amount: this.negotiatedPaymentAmount
      });
    }
  },
  async beforeMount() {
    await this.$store.dispatch("fetchInfluencerAds", this.influencerUsername);
  },
}
</script>

<style scoped>
body {
  background-color: #f8f9fa;
}

.content {
  margin-top: 2rem;
}

.blue i {
  color: #506582;
}

.btn-view {
  font-size: 0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 5px;
  margin: 0.2rem;
  font-weight: 600;
}

.btn a {
  font-size: 0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 5px;
  margin: 0.5rem;
  font-weight: 600;
}

.actions i {
  color: #506582;
  margin: 1rem;
}
</style>