export default {
    getAuth(state) {
        return {
            username: state.username,
            token: state.token,
            role: state.role,
            active: state.active,
        }
    },
    getStatus(state) {
        return {
            error: state.error,
            success: state.success,
            isLoggedIn: state.isLoggedIn
        }
    },
    getError(state){
      return state.error
    },
    greeting() {
      const hour = new Date().getHours();
      if (hour < 12) {
        return "Good morning";
      } else if (hour < 17) {
        return "Good afternoon";
      } else {
        return "Good evening";
      }
    },

    getInfluencers(state) {
        return state.influencers;
    },
    getSponsorCampaigns(state) {
        return state.sponsorCampaigns;
    },
    getCampaign(state){
        return state.campaign;
    },
    getCampaignAds(state){
        return state.campaignAds;
    },
    getAd(state){
        return state.ad;
    },
    getAdStatus(state){
        return state.adStatus;
    },

    // Influencer Actions
    getAllCampaigns(state){
        return state.allCampaigns;
    },
    getInfluencerAds(state){
        return state.influencerAds;
    },
    getInfluencerCampaigns(state){
        return state.influencerCampaigns;
    },
    getCeleryWaiting(state){
        return state.waiting;
    },
    getSearchResults(state){
        return state.searchResult
    },

    getSponsors(state){
        return state.sponsors;
    },
    getUserbaseData(state){
        return state.UserbaseData;
    },
    getCampaignData(state){
        return state.campaignData;
    },
    getAdsData(state){
        return state.adsData;
    }

}